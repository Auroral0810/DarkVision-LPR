import os
import shutil
import uuid
import cv2
import json
from datetime import datetime
from typing import Optional, List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.config import settings
from app.models.recognition import RecognitionRecord, RecognitionTask
from app.services.lpr.detection import PlateDetector
from app.services.lpr.enhancement import PlateEnhancer
from app.services.lpr.recognition import PlateRecognizer

from app.utils.oss import oss_uploader
import requests
import tempfile

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

    async def process_image_from_url(self, image_url: str, user_id: int, db: Session, task_id: int = None) -> Optional[RecognitionRecord]:
        """
        从OSS URL下载图片并进行识别
        """
        self._init_models()
        
        try:
            # Download image from URL
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            file_content = response.content
        except Exception as e:
            print(f"Failed to download image from URL: {e}")
            return None
            
        # Save locally temporarily for processing
        file_ext = os.path.splitext(image_url)[1] or '.jpg'
        filename = f"{uuid.uuid4()}{file_ext}"
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
            print(f"Detection failed: {e}")
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
            task_id=task_id,
            original_image_url=image_url,  # Use the OSS URL
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

    async def process_image(self, file: UploadFile, user_id: int, db: Session, task_id: int = None) -> Optional[RecognitionRecord]:
        """
        处理单张图片识别
        """
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
            print(f"OSS Upload failed, fallback to local or error: {e}")
            # Ensure upload dir exists
            upload_path = os.path.join(settings.UPLOAD_DIR, "original")
            os.makedirs(upload_path, exist_ok=True)
            file_path = os.path.join(upload_path, filename)
            with open(file_path, "wb") as buffer:
                buffer.write(file_content)
            oss_url = f"/uploads/original/{filename}"
            # Need to update logic to use local file for processing if OSS failed but local succeeded
            # But process logic below needs local file path anyway for opencv?
            
        # Save locally temporarily for processing (OpenCV needs file path usually, or decode from bytes)
        # It's better to process from bytes directly or save temp file
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
            print(f"Detection failed: {e}")
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
            task_id=task_id,
            original_image_url=oss_url,
            license_plate=plate_number,
            confidence=detection['conf'],
            bbox=list(detection['bbox']), # Convert tuple to list for JSON serialization
            plate_type="blue", # Placeholder logic, LPRNet doesn't classify color strictly yet
            processed_at=datetime.now()
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return record

recognition_service = RecognitionService()

