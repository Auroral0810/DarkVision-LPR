import cv2
import numpy as np

class PlateEnhancer:
    @staticmethod
    def rectify_plate_with_keypoints(img_rgb, keypoints, out_w=160, out_h=48):
        """
        使用关键点进行透视变换矫正车牌
        """
        # 源点（4个角点）
        src_pts = np.array(keypoints, dtype=np.float32)
        
        # 目标点（矩形）- 顺序：左上、右上、右下、左下
        dst_pts = np.array([
            [0, 0],
            [out_w - 1, 0],
            [out_w - 1, out_h - 1],
            [0, out_h - 1]
        ], dtype=np.float32)
        
        # 计算透视变换矩阵
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        
        # 应用透视变换
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        rectified = cv2.warpPerspective(img_bgr, M, (out_w, out_h))
        rectified_rgb = cv2.cvtColor(rectified, cv2.COLOR_BGR2RGB)
        
        return rectified_rgb

    @staticmethod
    def rectify_plate_with_bbox(img_rgb, bbox, out_w=160, out_h=48):
        """
        使用边界框裁剪车牌（当没有关键点时）
        """
        x1, y1, x2, y2 = bbox
        cropped = img_rgb[y1:y2, x1:x2]
        
        # 调整到目标尺寸
        resized = cv2.resize(cropped, (out_w, out_h))
        
        return resized

    @staticmethod
    def enhance_plate(plate_rgb):
        """
        图像增强处理
        Returns:
            enhanced_gray: 增强后的灰度图
            enhanced_binary: 增强后的二值图
        """
        # 转BGR（OpenCV处理）
        plate_bgr = cv2.cvtColor(plate_rgb, cv2.COLOR_RGB2BGR)
        
        # 1. 转灰度
        gray = cv2.cvtColor(plate_bgr, cv2.COLOR_BGR2GRAY)
        
        # 2. CLAHE对比度增强
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        clahe_img = clahe.apply(gray)
        
        # 3. 中值滤波去噪
        denoised = cv2.medianBlur(clahe_img, 3)
        
        # 4. Unsharp Mask锐化
        gaussian = cv2.GaussianBlur(denoised, (9, 9), 10.0)
        unsharp = cv2.addWeighted(denoised, 1.8, gaussian, -0.8, 0)
        
        # 5. 自适应二值化
        binary = cv2.adaptiveThreshold(
            unsharp, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # 6. 形态学开运算
        kernel_morph = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_morph, iterations=1)
        
        return unsharp, cleaned

