# -*- coding: utf-8 -*-
"""
完整的车牌识别流程
1. YOLO检测车牌区域和关键点
2. 透视变换矫正车牌
3. 图像增强
4. LPRNet识别车牌号码
5. 可视化展示整个过程
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch.autograd import Variable
from ultralytics import YOLO
from LPRNet import build_lprnet
import argparse
import os

# 定义车牌字符集
CHARS = ['京', '沪', '津', '渝', '冀', '晋', '蒙', '辽', '吉', '黑',
         '苏', '浙', '皖', '闽', '赣', '鲁', '豫', '鄂', '湘', '粤',
         '桂', '琼', '川', '贵', '云', '藏', '陕', '甘', '青', '宁',
         '新',
         '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K',
         'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
         'W', 'X', 'Y', 'Z', 'I', 'O', '-'
         ]

# 关键点配置
KPT_SHAPE = [4, 3]  # 4个关键点，每个点3个值(x, y, visibility)
KPT_NAMES = ['左上', '右上', '右下', '左下']


def get_parser():
    """参数配置"""
    parser = argparse.ArgumentParser(description='完整的车牌识别流程')
    
    # 输入图片
    parser.add_argument('--img_path', 
                       default='/Users/auroral/ProjectDevelopment/毕业设计/毕业论文/测试/01-92_83-296&480_459&554-463&554_304&535_291&472_450&491-0_0_22_32_17_27_29-111-8.jpg',
                       help='要识别的图片路径')
    
    # YOLO模型
    parser.add_argument('--yolo_model', 
                       default='/Users/auroral/ProjectDevelopment/毕业设计/毕业论文/测试/best.pt',
                       help='YOLO模型路径')
    parser.add_argument('--yolo_conf', default=0.25, type=float, help='YOLO检测置信度阈值')
    
    # LPRNet模型
    parser.add_argument('--lprnet_model', 
                       default='./Final_LPRNet_model.pth',
                       help='LPRNet模型路径')
    parser.add_argument('--lpr_max_len', default=8, type=int, help='车牌号码最大长度')
    parser.add_argument('--dropout_rate', default=0, type=float, help='dropout rate')
    
    # 透视变换参数
    parser.add_argument('--rect_width', default=160, type=int, help='矫正后车牌宽度')
    parser.add_argument('--rect_height', default=48, type=int, help='矫正后车牌高度')
    
    # LPRNet输入尺寸
    parser.add_argument('--lprnet_width', default=94, type=int, help='LPRNet输入宽度')
    parser.add_argument('--lprnet_height', default=24, type=int, help='LPRNet输入高度')
    
    # 其他参数
    parser.add_argument('--cuda', default=True, type=bool, help='是否使用GPU')
    parser.add_argument('--show', default=True, type=bool, help='是否显示可视化结果')
    
    return parser.parse_args()


def detect_plate_with_yolo(model, image_path, conf_threshold=0.25):
    """
    使用YOLO检测车牌区域和关键点
    
    Returns:
        img_rgb: RGB格式的原图
        detections: 检测结果列表，每个元素包含 (bbox, conf, cls_name, keypoints)
    """
    print("\n[步骤1] YOLO检测车牌区域...")
    
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"无法读取图片: {image_path}")
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(f"  原始图片尺寸: {img.shape}")
    
    # YOLO推理
    results = model(image_path, conf=conf_threshold, verbose=False)
    
    detections = []
    for i, box in enumerate(results[0].boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
        conf = float(box.conf[0].cpu().numpy())
        cls_id = int(box.cls[0].cpu().numpy())
        cls_name = results[0].names[cls_id]
        
        # 提取关键点（如果有）
        keypoints = None
        if hasattr(results[0], 'keypoints') and results[0].keypoints is not None:
            # 获取完整的关键点数据，包括visibility
            kpts_data = results[0].keypoints[i].data[0].cpu().numpy()  # shape: [4, 3]
            if len(kpts_data) == 4:  # 4个角点
                # 提取xy坐标（忽略visibility），shape: [4, 2]
                keypoints = kpts_data[:, :2]
        
        print(f"  检测到车牌 {i + 1}:")
        print(f"    类别: {cls_name}, 置信度: {conf:.4f}")
        print(f"    边界框: ({x1}, {y1}) - ({x2}, {y2})")
        if keypoints is not None:
            print(f"    关键点数量: {len(keypoints)}")
            for kpt_idx, (x, y) in enumerate(keypoints):
                print(f"      {KPT_NAMES[kpt_idx]}: ({x:.1f}, {y:.1f})")
        
        detections.append({
            'bbox': (x1, y1, x2, y2),
            'conf': conf,
            'cls_name': cls_name,
            'keypoints': keypoints
        })
    
    return img_rgb, detections


def rectify_plate_with_keypoints(img_rgb, keypoints, out_w=160, out_h=48):
    """
    使用关键点进行透视变换矫正车牌
    
    Args:
        img_rgb: RGB格式的图片
        keypoints: 4个角点坐标 [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
        out_w: 输出宽度
        out_h: 输出高度
    
    Returns:
        rectified: 矫正后的车牌图像
    """
    print("\n[步骤2] 透视变换矫正车牌...")
    
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
    
    print(f"  矫正后尺寸: {rectified_rgb.shape}")
    
    return rectified_rgb


def rectify_plate_with_bbox(img_rgb, bbox, out_w=160, out_h=48):
    """
    使用边界框裁剪车牌（当没有关键点时）
    
    Args:
        img_rgb: RGB格式的图片
        bbox: (x1, y1, x2, y2)
        out_w: 输出宽度
        out_h: 输出高度
    
    Returns:
        cropped: 裁剪并调整大小后的车牌图像
    """
    print("\n[步骤2] 使用边界框裁剪车牌...")
    
    x1, y1, x2, y2 = bbox
    cropped = img_rgb[y1:y2, x1:x2]
    
    # 调整到目标尺寸
    resized = cv2.resize(cropped, (out_w, out_h))
    
    print(f"  裁剪后尺寸: {resized.shape}")
    
    return resized


def enhance_plate(plate_rgb):
    """
    图像增强处理
    
    Args:
        plate_rgb: RGB格式的车牌图像
    
    Returns:
        enhanced_gray: 增强后的灰度图
        enhanced_binary: 增强后的二值图
    """
    print("\n[步骤3] 图像增强处理...")
    
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
    
    print(f"  增强处理完成")
    
    return unsharp, cleaned


def transform_for_lprnet(img):
    """LPRNet图片预处理"""
    img = img.astype('float32')
    img -= 127.5
    img *= 0.0078125
    img = np.transpose(img, (2, 0, 1))
    return img


def greedy_decode(preb):
    """Greedy解码，将模型输出转换为车牌号码"""
    preb_label = list()
    for j in range(preb.shape[1]):
        preb_label.append(np.argmax(preb[:, j], axis=0))
    
    no_repeat_blank_label = list()
    pre_c = preb_label[0]
    if pre_c != len(CHARS) - 1:  # 如果不是空白字符
        no_repeat_blank_label.append(pre_c)
    
    for c in preb_label:  # 去除重复标签和空白标签
        if (pre_c == c) or (c == len(CHARS) - 1):
            if c == len(CHARS) - 1:
                pre_c = c
            continue
        no_repeat_blank_label.append(c)
        pre_c = c
    
    return no_repeat_blank_label


def recognize_plate_with_lprnet(lprnet, plate_img, lprnet_width=94, lprnet_height=24, use_cuda=True):
    """
    使用LPRNet识别车牌号码
    
    Args:
        lprnet: LPRNet模型
        plate_img: 车牌图像（RGB或BGR，会被调整为LPRNet输入尺寸）
        lprnet_width: LPRNet输入宽度
        lprnet_height: LPRNet输入高度
        use_cuda: 是否使用GPU
    
    Returns:
        plate_number: 识别的车牌号码字符串
        lprnet_input: 用于可视化的LPRNet输入图像
    """
    print("\n[步骤4] LPRNet识别车牌号码...")
    
    # 确保是BGR格式（OpenCV）
    if len(plate_img.shape) == 2:  # 灰度图
        plate_bgr = cv2.cvtColor(plate_img, cv2.COLOR_GRAY2BGR)
    elif plate_img.shape[2] == 3:
        # 假设输入是RGB，转为BGR
        plate_bgr = cv2.cvtColor(plate_img, cv2.COLOR_RGB2BGR)
    else:
        plate_bgr = plate_img
    
    # 调整到LPRNet输入尺寸
    img_resized = cv2.resize(plate_bgr, (lprnet_width, lprnet_height))
    lprnet_input = img_resized.copy()
    
    # 预处理
    img_processed = transform_for_lprnet(img_resized)
    img_tensor = torch.from_numpy(img_processed).unsqueeze(0)  # 添加batch维度
    
    # 推理
    lprnet.eval()
    with torch.no_grad():
        if use_cuda and torch.cuda.is_available():
            img_tensor = Variable(img_tensor.cuda())
        else:
            img_tensor = Variable(img_tensor)
        
        # 前向传播
        prebs = lprnet(img_tensor)
        prebs = prebs.cpu().detach().numpy()
    
    # 解码
    preb = prebs[0, :, :]
    label = greedy_decode(preb)
    
    # 转换为车牌号码字符串
    plate_number = ""
    for i in label:
        plate_number += CHARS[i]
    
    print(f"  识别结果: {plate_number}")
    
    return plate_number, cv2.cvtColor(lprnet_input, cv2.COLOR_BGR2RGB)


def visualize_pipeline(img_rgb, detection, rectified, enhanced_gray, enhanced_binary, 
                       lprnet_input, plate_number):
    """
    可视化整个处理流程
    
    Args:
        img_rgb: 原始图片（带检测框）
        detection: 检测结果
        rectified: 矫正后的车牌
        enhanced_gray: 增强后的灰度图
        enhanced_binary: 增强后的二值图
        lprnet_input: LPRNet输入图像
        plate_number: 识别的车牌号码
    """
    print("\n[步骤5] 可视化展示...")
    
    # 在原图上绘制检测框和关键点
    img_display = img_rgb.copy()
    x1, y1, x2, y2 = detection['bbox']
    
    # 绘制边界框
    cv2.rectangle(img_display, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # 绘制关键点
    if detection['keypoints'] is not None:
        for kp in detection['keypoints']:
            cv2.circle(img_display, (int(kp[0]), int(kp[1])), 5, (255, 0, 0), -1)
    
    # 绘制置信度和类别
    cv2.putText(img_display, 
                f"{detection['cls_name']} {detection['conf']:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 0, 0), 2)
    
    # 创建可视化
    plt.figure(figsize=(18, 10))
    
    # 1. 原图 + 检测结果
    plt.subplot(2, 3, 1)
    plt.imshow(img_display)
    plt.title("1. YOLO检测结果", fontsize=12, fontproperties='SimHei')
    plt.axis('off')
    
    # 2. 矫正后的车牌
    plt.subplot(2, 3, 2)
    plt.imshow(rectified)
    plt.title("2. 透视变换矫正", fontsize=12, fontproperties='SimHei')
    plt.axis('off')
    
    # 3. 增强后的灰度图
    plt.subplot(2, 3, 3)
    plt.imshow(enhanced_gray, cmap='gray')
    plt.title("3. 图像增强（灰度）", fontsize=12, fontproperties='SimHei')
    plt.axis('off')
    
    # 4. 增强后的二值图
    plt.subplot(2, 3, 4)
    plt.imshow(enhanced_binary, cmap='gray')
    plt.title("4. 图像增强（二值化）", fontsize=12, fontproperties='SimHei')
    plt.axis('off')
    
    # 5. LPRNet输入
    plt.subplot(2, 3, 5)
    plt.imshow(lprnet_input)
    plt.title("5. LPRNet输入 (94x24)", fontsize=12, fontproperties='SimHei')
    plt.axis('off')
    
    # 6. 最终识别结果
    plt.subplot(2, 3, 6)
    plt.text(0.5, 0.5, plate_number, 
             fontsize=36, ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.title("6. 识别结果", fontsize=12, fontproperties='SimHei')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('pipeline_result.png', dpi=150, bbox_inches='tight')
    print("  可视化结果已保存到: pipeline_result.png")
    plt.show()


def main():
    """主流程"""
    args = get_parser()
    
    print("=" * 80)
    print("完整的车牌识别流程")
    print("=" * 80)
    
    # 检查文件是否存在
    if not os.path.exists(args.img_path):
        print(f"[错误] 图片文件不存在: {args.img_path}")
        return
    
    if not os.path.exists(args.yolo_model):
        print(f"[错误] YOLO模型文件不存在: {args.yolo_model}")
        return
    
    if not os.path.exists(args.lprnet_model):
        print(f"[错误] LPRNet模型文件不存在: {args.lprnet_model}")
        return
    
    # ========== 加载模型 ==========
    print("\n[初始化] 加载模型...")
    
    # 加载YOLO模型
    yolo_model = YOLO(args.yolo_model)
    # 设置kpt_shape属性
    if hasattr(yolo_model, 'model'):
        yolo_model.model.kpt_shape = KPT_SHAPE
        print(f"  ✓ YOLO模型加载成功（已设置 kpt_shape: {KPT_SHAPE}）")
    else:
        print(f"  ✓ YOLO模型加载成功")
    
    # 加载LPRNet模型
    device = torch.device("cuda:0" if args.cuda and torch.cuda.is_available() else "cpu")
    lprnet = build_lprnet(
        lpr_max_len=args.lpr_max_len,
        phase=False,
        class_num=len(CHARS),
        dropout_rate=args.dropout_rate
    )
    lprnet.to(device)
    lprnet.load_state_dict(torch.load(args.lprnet_model, map_location=device))
    print(f"  ✓ LPRNet模型加载成功（设备: {device}）")
    
    # ========== 执行识别流程 ==========
    
    # 步骤1: YOLO检测车牌
    img_rgb, detections = detect_plate_with_yolo(yolo_model, args.img_path, args.yolo_conf)
    
    if len(detections) == 0:
        print("\n[警告] 未检测到车牌！")
        return
    
    # 处理第一个检测到的车牌
    detection = detections[0]
    
    # 步骤2: 透视变换矫正车牌
    if detection['keypoints'] is not None and len(detection['keypoints']) == 4:
        # 使用关键点进行透视变换
        rectified = rectify_plate_with_keypoints(
            img_rgb, 
            detection['keypoints'],
            args.rect_width, 
            args.rect_height
        )
    else:
        # 使用边界框裁剪
        rectified = rectify_plate_with_bbox(
            img_rgb,
            detection['bbox'],
            args.rect_width,
            args.rect_height
        )
    
    # 步骤3: 图像增强
    enhanced_gray, enhanced_binary = enhance_plate(rectified)
    
    # 步骤4: LPRNet识别
    plate_number, lprnet_input = recognize_plate_with_lprnet(
        lprnet,
        rectified,
        args.lprnet_width,
        args.lprnet_height,
        args.cuda and torch.cuda.is_available()
    )
    
    # 步骤5: 可视化
    if args.show:
        visualize_pipeline(
            img_rgb,
            detection,
            rectified,
            enhanced_gray,
            enhanced_binary,
            lprnet_input,
            plate_number
        )
    
    print("\n" + "=" * 80)
    print(f"最终识别结果: {plate_number}")
    print("=" * 80)
    
    return plate_number


if __name__ == "__main__":
    main()

