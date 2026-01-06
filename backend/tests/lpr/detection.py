import cv2
import numpy as np
from ultralytics import YOLO
from app.services.lpr.constants import KPT_SHAPE, KPT_NAMES
import os
import sys

class PlateDetector:
    def __init__(self, model_path: str, conf_threshold: float = 0.25):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"YOLO model not found at {model_path}")
        
        try:
            self.model = YOLO(model_path)
        except AttributeError as e:
            if "'C3k2'" in str(e):
                raise RuntimeError(
                    "Failed to load YOLO model due to version mismatch. "
                    "The model requires a newer version of 'ultralytics'. "
                    "Please upgrade by running: pip install --upgrade ultralytics"
                ) from e
            raise e
            
        # Initialize KPT_SHAPE if needed (though ultralytics usually handles this)
        if hasattr(self.model, 'model') and hasattr(self.model.model, 'kpt_shape'):
            self.model.model.kpt_shape = KPT_SHAPE
        self.conf_threshold = conf_threshold

    def detect(self, img_path: str):
        """
        使用YOLO检测车牌区域和关键点
        
        Returns:
            img_rgb: RGB格式的原图
            detections: 检测结果列表，每个元素包含 (bbox, conf, cls_name, keypoints)
        """
        # 读取图片
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"无法读取图片: {img_path}")
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # YOLO推理
        results = self.model(img_path, conf=self.conf_threshold, verbose=False)
        
        detections = []
        for i, box in enumerate(results[0].boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            conf = float(box.conf[0].cpu().numpy())
            cls_id = int(box.cls[0].cpu().numpy())
            cls_name = results[0].names[cls_id]
            
            # 提取关键点（如果有）
            keypoints = None
            if hasattr(results[0], 'keypoints') and results[0].keypoints is not None:
                # 获取完整的关键点数据
                # Check for different ultralytics versions (some use .xy, some .data, some .cpu().numpy())
                if hasattr(results[0].keypoints[i], 'data'):
                    kpts_data = results[0].keypoints[i].data[0].cpu().numpy()  # shape: [4, 3]
                elif hasattr(results[0].keypoints[i], 'xy'):
                    kpts_data = results[0].keypoints[i].xy[0].cpu().numpy()
                else:
                    kpts_data = []

                if len(kpts_data) == 4:  # 4个角点
                    # 提取xy坐标（忽略visibility），shape: [4, 2]
                    # Check dim
                    if kpts_data.shape[-1] >= 2:
                        keypoints = kpts_data[:, :2]
            
            detections.append({
                'bbox': (x1, y1, x2, y2),
                'conf': conf,
                'cls_name': cls_name,
                'keypoints': keypoints
            })
        
        return img_rgb, detections
