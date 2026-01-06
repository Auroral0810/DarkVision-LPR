import os
import shutil
import uuid
import cv2
import json
import asyncio
from datetime import datetime, date
from typing import Optional, List
from fastapi import UploadFile, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.config import settings
from app.models.recognition import RecognitionRecord, RecognitionTask, RecognitionStatistic
from app.services.lpr.detection import PlateDetector
from app.services.lpr.enhancement import PlateEnhancer
from app.services.lpr.recognition import PlateRecognizer
from app.services.websocket_manager import manager

from app.utils.oss import oss_uploader
import requests
import tempfile
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

# Helper to run CPU bound tasks
async def run_cpu_bound(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

class RecognitionService:
    def __init__(self):
        # Lazy loading models
        self.detector = None
        self.recognizer = None
        
    def _init_models(self):
        if not self.detector:
            print(f"Loading YOLO model from {settings.YOLO_MODEL_PATH}...")
            self.detector = PlateDetector(settings.YOLO_MODEL_PATH)
        if not self.recognizer:
            print(f"Loading LPRNet model from {settings.LPRNET_MODEL_PATH}...")
            self.recognizer = PlateRecognizer(settings.LPRNET_MODEL_PATH)

    def check_quota(self, user_id: int, db: Session) -> bool:
        """检查用户今日是否有剩余额度"""
        today = date.today()
        stat = db.query(RecognitionStatistic).filter(
            RecognitionStatistic.user_id == user_id,
            RecognitionStatistic.stat_date == today
        ).first()
        return True

    def deduct_quota(self, user_id: int, db: Session):
        """扣除额度（增加使用计数）"""
        today = date.today()
        stat = db.query(RecognitionStatistic).filter(
            RecognitionStatistic.user_id == user_id,
            RecognitionStatistic.stat_date == today
        ).first()
        
        if not stat:
            stat = RecognitionStatistic(
                user_id=user_id,
                stat_date=today,
                daily_count=1,
                monthly_count=1 # Simplified, implies first of month logic needed elsewhere or just counter
            )
            db.add(stat)
        else:
            stat.daily_count += 1
            stat.monthly_count += 1
            
        db.commit()

    def create_task(self, user_id: int, task_type: str, db: Session) -> RecognitionTask:
        """创建识别任务"""
        task_uuid = str(uuid.uuid4())
        task = RecognitionTask(
            task_uuid=task_uuid,
            user_id=user_id,
            task_type=task_type,
            status='pending',
            progress=0.00,
            total_items=1
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    async def update_task_progress(self, task_uuid: str, progress: float, status: str, db: Session, message: str = ""):
        """更新任务进度并推送WS消息"""
        logger.info(f"Updating task {task_uuid}: {progress}% - {status}")
        # Push to WebSocket
        await manager.broadcast_to_task(task_uuid, {
            "type": "progress",
            "progress": progress,
            "status": status,
            "message": message
        })

    async def process_task_async(self, task_uuid: str, image_url: str, user_id: int):
        """异步处理识别任务"""
        from app.core.database import SessionLocal
        db = SessionLocal()
        
        logger.info(f"Starting async processing for task {task_uuid}")
        
        # Give frontend time to connect WebSocket
        # Wait slightly less to ensure we don't delay too much if client is fast
        await asyncio.sleep(1.0)
        
        try:
            task = db.query(RecognitionTask).filter(RecognitionTask.task_uuid == task_uuid).first()
            if not task:
                logger.error(f"Task {task_uuid} not found")
                return

            task.status = 'processing'
            task.started_at = datetime.now()
            db.commit()
            
            await self.update_task_progress(task_uuid, 25, "downloading", db, "图片上传成功，正在下载...")
            
            # 1. Download
            # Run blocking model init in executor
            await run_cpu_bound(self._init_models)
            
            try:
                # Handle local path vs URL
                if image_url.startswith('http'):
                    # Check if it's our own OSS URL
                    oss_url_prefix = settings.OSS_URL
                    if oss_url_prefix and oss_url_prefix in image_url:
                         # Extract object key
                         object_key = image_url.replace(oss_url_prefix, "")
                         if object_key.startswith("/"):
                             object_key = object_key[1:]
                             
                         try:
                             # Use executor for OSS operations (network IO/crypto)
                             file_content = await run_cpu_bound(oss_uploader.get_file_content, object_key)
                         except Exception as oss_e:
                             logger.error(f"OSS Direct Download failed: {oss_e}, falling back to HTTP")
                             response = await run_cpu_bound(requests.get, image_url, timeout=15)
                             response.raise_for_status()
                             file_content = response.content
                    else:
                        response = await run_cpu_bound(requests.get, image_url, timeout=15)
                        response.raise_for_status()
                        file_content = response.content
                else:
                     with open(image_url, 'rb') as f:
                        file_content = f.read()

            except Exception as e:
                raise Exception(f"Download/Read failed: {str(e)}")

            await self.update_task_progress(task_uuid, 50, "detecting", db, "正在进行车牌检测...")
            
            # Save temp
            file_ext = '.jpg'
            filename = f"{uuid.uuid4()}{file_ext}"
            upload_path = os.path.join(settings.UPLOAD_DIR, "temp")
            os.makedirs(upload_path, exist_ok=True)
            temp_file_path = os.path.join(upload_path, filename)
            
            with open(temp_file_path, "wb") as buffer:
                buffer.write(file_content)

            # 2. Detection (CPU Bound)
            try:
                img_rgb, detections = await run_cpu_bound(self.detector.detect, temp_file_path)
            except Exception as e:
                if os.path.exists(temp_file_path): os.remove(temp_file_path)
                raise Exception(f"Detection failed: {str(e)}")

            if not detections:
                if os.path.exists(temp_file_path): os.remove(temp_file_path)
                raise Exception("未检测到车牌")

            await self.update_task_progress(task_uuid, 75, "enhancing", db, "正在进行图像增强...")
            
            # Process best detection
            detection = detections[0]
            
            # 3. Enhancement (CPU Bound)
            if detection['keypoints'] is not None:
                rectified = await run_cpu_bound(PlateEnhancer.rectify_plate_with_keypoints, img_rgb, detection['keypoints'])
            else:
                rectified = await run_cpu_bound(PlateEnhancer.rectify_plate_with_bbox, img_rgb, detection['bbox'])

            await self.update_task_progress(task_uuid, 90, "recognizing", db, "正在识别字符...")

            # 4. Recognition (CPU Bound)
            plate_number, _ = await run_cpu_bound(self.recognizer.recognize, rectified)
            
            # Cleanup
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

            # Save Record
            record = RecognitionRecord(
                task_id=task.id,
                user_id=user_id,
                original_image_url=image_url,
                license_plate=plate_number,
                confidence=float(detection['conf']),
                bbox=detection['bbox'], # SQLAlchemy JSON type handles list/dict
                plate_type="blue", # Placeholder
                processed_at=datetime.now()
            )
            db.add(record)
            
            # Update Task
            task.status = 'completed'
            task.progress = 100.00
            task.success_count = 1
            task.finished_at = datetime.now()
            db.commit()
            db.refresh(record)

            # Push Final Result
            result_data = {
                "type": "result",
                "progress": 100,
                "status": "completed",
                "message": "识别成功",
                "data": {
                    "plate": plate_number,
                    "type": "blue", # TODO: Determine type
                    "confidence": f"{float(detection['conf'])*100:.1f}",
                    "image_url": image_url
                }
            }
            
            # Add delay to ensure transaction committed and WS open
            await asyncio.sleep(0.5)
            await manager.broadcast_to_task(task_uuid, result_data)

        except Exception as e:
            logger.error(f"Task {task_uuid} failed: {e}")
            # Refresh task to avoid stale state if commit failed previously
            db.rollback()
            task = db.query(RecognitionTask).filter(RecognitionTask.task_uuid == task_uuid).first()
            if task:
                task.status = 'failed'
                task.failed_count = 1
                task.finished_at = datetime.now()
                db.commit()
            
            await manager.broadcast_to_task(task_uuid, {
                "type": "error",
                "status": "failed",
                "message": str(e)
            })
        finally:
            db.close()

    async def process_image(self, file: UploadFile, user_id: int, db: Session) -> Optional[RecognitionRecord]:
        """Keep legacy method for backward compatibility if needed, or redirect to async logic"""
        # ... (Legacy logic can remain or be refactored to use the same pipeline)
        # For this refactor, we focus on process_task_async
        return await self._process_image_legacy(file, user_id, db)

    async def _process_image_legacy(self, file: UploadFile, user_id: int, db: Session) -> Optional[RecognitionRecord]:
        self._init_models()
        
        # Read file content
        file_content = await file.read()
        
        # Save file to OSS
        file_ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_ext}"
        
        try:
            # Upload to OSS
            oss_url = oss_uploader.upload_file(file_content, f"lpr/original/{filename}")
        except Exception as e:
            logger.error(f"OSS Upload failed: {e}")
            # Ensure upload dir exists
            upload_path = os.path.join(settings.UPLOAD_DIR, "original")
            os.makedirs(upload_path, exist_ok=True)
            file_path = os.path.join(upload_path, filename)
            with open(file_path, "wb") as buffer:
                buffer.write(file_content)
            oss_url = f"/uploads/original/{filename}"
            
        # Save locally temporarily for processing
        upload_path = os.path.join(settings.UPLOAD_DIR, "temp")
        os.makedirs(upload_path, exist_ok=True)
        temp_file_path = os.path.join(upload_path, filename)
        with open(temp_file_path, "wb") as buffer:
            buffer.write(file_content)
            
        # Run Pipeline
        # 1. Detection
        try:
            img_rgb, detections = self.detector.detect(temp_file_path)
        except Exception as e:
            logger.error(f"Detection failed: {e}")
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            return None
        
        if not detections:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            return None # No plate detected
            
        # For now, process the first detection (highest confidence)
        detection = detections[0]
        
        # 2. Enhancement
        if detection['keypoints'] is not None:
             rectified = PlateEnhancer.rectify_plate_with_keypoints(img_rgb, detection['keypoints'])
        else:
             rectified = PlateEnhancer.rectify_plate_with_bbox(img_rgb, detection['bbox'])
             
        # 3. Recognition
        plate_number, _ = self.recognizer.recognize(rectified)
        
        # Clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        # Save to DB
        record = RecognitionRecord(
            user_id=user_id,
            original_image_url=oss_url,
            license_plate=plate_number,
            confidence=detection['conf'],
            bbox=list(detection['bbox']),
            plate_type="blue",
            processed_at=datetime.now()
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return record
    
    def get_history(
        self, 
        user_id: int, 
        db: Session,
        page: int = 1,
        page_size: int = 10,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        license_plate: Optional[str] = None,
        plate_type: Optional[str] = None
    ):
        """获取识别历史记录"""
        query = db.query(RecognitionRecord).filter(RecognitionRecord.user_id == user_id)
        
        if start_date:
            query = query.filter(RecognitionRecord.created_at >= start_date)
        if end_date:
            query = query.filter(RecognitionRecord.created_at <= end_date)
        if license_plate:
            query = query.filter(RecognitionRecord.license_plate.like(f"%{license_plate}%"))
        if plate_type:
            query = query.filter(RecognitionRecord.plate_type == plate_type)
            
        total = query.count()
        
        # Sort by creation time desc
        query = query.order_by(RecognitionRecord.created_at.desc())
        
        # Pagination
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return items, total

recognition_service = RecognitionService()
