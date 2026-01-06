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

    async def process_image(self, file: UploadFile, user_id: int, db: Session, task_id: int = None) -> Optional[RecognitionRecord]:
        """
        处理单张图片识别
        """
        self._init_models()
        
        # Ensure upload dir exists
        upload_path = os.path.join(settings.UPLOAD_DIR, "original")
        os.makedirs(upload_path, exist_ok=True)
        
        # Save file
        file_ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(upload_path, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Run Pipeline
        # 1. Detection
        try:
            img_rgb, detections = self.detector.detect(file_path)
        except Exception as e:
            print(f"Detection failed: {e}")
            return None
        
        if not detections:
            return None # No plate detected
            
        # For now, process the first detection (highest confidence)
        detection = detections[0]
        
        # 2. Enhancement
        if detection['keypoints'] is not None:
             rectified = PlateEnhancer.rectify_plate_with_keypoints(img_rgb, detection['keypoints'])
        else:
             rectified = PlateEnhancer.rectify_plate_with_bbox(img_rgb, detection['bbox'])
             
        # Optional: Save enhanced image?
        # For now we just use it for recognition
        
        # 3. Recognition
        plate_number, _ = self.recognizer.recognize(rectified)
        
        # Save to DB
        # Generate relative URL for frontend
        relative_url = f"/uploads/original/{filename}"
        
        record = RecognitionRecord(
            user_id=user_id,
            task_id=task_id,
            original_image_url=relative_url,
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

