import torch
import cv2
import numpy as np
from torch.autograd import Variable
from app.services.lpr.lprnet_model import build_lprnet
from app.services.lpr.constants import CHARS
import os

class PlateRecognizer:
    def __init__(self, model_path: str, lpr_max_len=8, use_cuda=True):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"LPRNet model not found at {model_path}")
            
        self.device = torch.device("cuda:0" if use_cuda and torch.cuda.is_available() else "cpu")
        self.lprnet = build_lprnet(
            lpr_max_len=lpr_max_len,
            phase=False,
            class_num=len(CHARS),
            dropout_rate=0 # Eval mode
        )
        self.lprnet.to(self.device)
        self.lprnet.load_state_dict(torch.load(model_path, map_location=self.device))
        self.lprnet.eval()
        self.lprnet_width = 94
        self.lprnet_height = 24

    def transform_for_lprnet(self, img):
        """LPRNet图片预处理"""
        img = img.astype('float32')
        img -= 127.5
        img *= 0.0078125
        img = np.transpose(img, (2, 0, 1))
        return img

    def greedy_decode(self, preb):
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

    def recognize(self, plate_img):
        """
        使用LPRNet识别车牌号码
        
        Args:
            plate_img: 车牌图像（RGB或BGR，会被调整为LPRNet输入尺寸）
            
        Returns:
            plate_number: 识别的车牌号码字符串
            lprnet_input_rgb: 用于可视化的LPRNet输入图像
        """
        # 确保是BGR格式（OpenCV）
        if len(plate_img.shape) == 2:  # 灰度图
            plate_bgr = cv2.cvtColor(plate_img, cv2.COLOR_GRAY2BGR)
        elif plate_img.shape[2] == 3:
            # 假设输入是RGB，转为BGR (如果OpenCV read则已经是BGR，但如果是PIL转的numpy可能是RGB)
            # 在detection中我们转成了RGB，这里如果传入的是RGB
            plate_bgr = cv2.cvtColor(plate_img, cv2.COLOR_RGB2BGR)
        else:
            plate_bgr = plate_img
        
        # 调整到LPRNet输入尺寸
        img_resized = cv2.resize(plate_bgr, (self.lprnet_width, self.lprnet_height))
        lprnet_input = img_resized.copy()
        
        # 预处理
        img_processed = self.transform_for_lprnet(img_resized)
        img_tensor = torch.from_numpy(img_processed).unsqueeze(0)  # 添加batch维度
        
        # 推理
        with torch.no_grad():
            img_tensor = Variable(img_tensor.to(self.device))
            
            # 前向传播
            prebs = self.lprnet(img_tensor)
            prebs = prebs.cpu().detach().numpy()
        
        # 解码
        preb = prebs[0, :, :]
        label = self.greedy_decode(preb)
        
        # 转换为车牌号码字符串
        plate_number = ""
        for i in label:
            plate_number += CHARS[i]
        
        return plate_number, cv2.cvtColor(lprnet_input, cv2.COLOR_BGR2RGB)

