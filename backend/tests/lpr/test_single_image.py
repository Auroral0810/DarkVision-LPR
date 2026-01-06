import os
import cv2
import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont
from detection import PlateDetector
from recognition import PlateRecognizer
from enhancement import PlateEnhancer

def draw_chinese_text(img, text, position, font_path, font_size=30, color=(0, 255, 0)):
    """在图片上绘制中文字符"""
    # 转换为PIL格式
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"Warning: Could not load font {font_path}, falling back to default. Error: {e}")
        font = ImageFont.load_default()
    
    # 绘制文字
    draw.text(position, text, font=font, fill=color)
    
    # 转回OpenCV格式
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def visualize_enhancement(before_rgb, after_gray, after_binary, save_path):
    """可视化增强前后的对比"""
    # 统一尺寸
    h, w = before_rgb.shape[:2]
    
    # 转换灰度图和二值图为3通道，以便拼接
    after_gray_bgr = cv2.cvtColor(after_gray, cv2.COLOR_GRAY2BGR)
    after_binary_bgr = cv2.cvtColor(after_binary, cv2.COLOR_GRAY2BGR)
    
    # 拼接：原图 | 增强灰度 | 二值化
    combined = np.hstack((cv2.cvtColor(before_rgb, cv2.COLOR_RGB2BGR), after_gray_bgr, after_binary_bgr))
    
    # 添加标题（简单处理，因为拼接图通常较小）
    cv2.imwrite(save_path, combined)
    print(f"  - Enhancement comparison saved to {save_path}")

def main():
    # 路径配置
    img_path = "/Users/auroral/ProjectDevelopment/DarkVision-LPR/backend/tests/lpr/041125478927203064-94_258-48&539_325&675-325&675_59&636_48&539_316&564-0_0_3_33_33_24_30_30-64-512.jpg"
    results_dir = "/Users/auroral/ProjectDevelopment/DarkVision-LPR/backend/tests/lpr/results"
    yolo_model_path = "/Users/auroral/ProjectDevelopment/DarkVision-LPR/backend/weights/best.pt"
    lprnet_model_path = "/Users/auroral/ProjectDevelopment/DarkVision-LPR/backend/weights/Final_LPRNet_model.pth"
    font_path = "/Library/Fonts/SimHei.ttf" # 已确认存在的字体

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    print(f"Loading models...")
    detector = PlateDetector(yolo_model_path)
    recognizer = PlateRecognizer(lprnet_model_path)
    enhancer = PlateEnhancer()

    print(f"Processing image: {img_path}")
    img_rgb, detections = detector.detect(img_path)
    
    # 1. 打印YOLO结果
    print("-" * 30)
    print(f"YOLO detection results (Total: {len(detections)}):")
    for i, det in enumerate(detections):
        print(f"[{i+1}] Box: {det['bbox']}, Conf: {det['conf']:.4f}, Class: {det['cls_name']}")
    print("-" * 30)

    # 绘制基础图
    img_bgr_visual = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    if not detections:
        print("No plates detected.")
        return

    for i, det in enumerate(detections):
        bbox = det['bbox']
        keypoints = det['keypoints']
        conf = det['conf']
        
        # 2. 剪裁和投射变换可视化
        if keypoints is not None:
            rectified_rgb = enhancer.rectify_plate_with_keypoints(img_rgb, keypoints)
            method = "keypoints"
        else:
            rectified_rgb = enhancer.rectify_plate_with_bbox(img_rgb, bbox)
            method = "bbox"
            
        rectified_bgr = cv2.cvtColor(rectified_rgb, cv2.COLOR_RGB2BGR)
        rect_save_path = os.path.join(results_dir, f"plate_{i+1}_rectified.jpg")
        cv2.imwrite(rect_save_path, rectified_bgr)
        print(f"  - Rectified image (via {method}) saved to {rect_save_path}")

        # 3. 图像增强前后对比可视化
        enhanced_gray, enhanced_binary = enhancer.enhance_plate(rectified_rgb)
        enhancement_save_path = os.path.join(results_dir, f"plate_{i+1}_enhancement_compare.jpg")
        visualize_enhancement(rectified_rgb, enhanced_gray, enhanced_binary, enhancement_save_path)

        # 4. LPRNet识别过程和最终结果可视化
        # 识别
        plate_number, _ = recognizer.recognize(rectified_rgb)
        print(f"  - Recognized plate number: {plate_number}")

        # 在原图上可视化 (使用中文字体)
        x1, y1, x2, y2 = bbox
        cv2.rectangle(img_bgr_visual, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # 绘制关键点
        if keypoints is not None:
            for kp in keypoints:
                cv2.circle(img_bgr_visual, (int(kp[0]), int(kp[1])), 5, (0, 0, 255), -1)

        # 绘制中文文字信息
        display_text = f"{plate_number} ({conf:.2f})"
        img_bgr_visual = draw_chinese_text(img_bgr_visual, display_text, (x1, y1 - 40), font_path, font_size=25)

    # 保存最终大图结果
    final_output_path = os.path.join(results_dir, "final_recognition_result.jpg")
    cv2.imwrite(final_output_path, img_bgr_visual)
    print(f"Final visualization result saved to {final_output_path}")
    print("-" * 30)
    print("Process completed successfully.")

if __name__ == "__main__":
    main()
