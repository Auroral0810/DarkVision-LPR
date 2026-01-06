# Deep Learning Model

The core competitiveness of DarkVision-LPR lies in its AI algorithm pipeline optimized for **low-light scenarios**.

## Algorithm Pipeline

The system adopts a serial processing flow:

1. **Retinex Image Enhancement**: First, applies light compensation to the input image.
2. **YOLOv11m Vehicle Detection**: Localizes vehicles and license plate areas.
3. **LPRNet Character Recognition**: Performs sequence recognition on the cropped license plate area.

## 1. Object Detection: YOLOv11m

We chose the **YOLOv11m (Medium)** version as the core detector because:
- **Speed & Accuracy Balance**: Higher accuracy than Nano/Small versions, faster than Large versions, suitable for real-time stream processing.
- **Small Object Optimization**: Better recall rate for distant, small license plates.

### Training Details
- **Dataset**: A mix of CCPD2019, CCPD2020, and self-collected low-light datasets, totaling **30,000+** images.
- **Augmentation**: Mosaic, Mixup, RandomBrightness (simulating more dark environments).
- **Result**: mAP@0.5:0.95 achieved **99.9%**.

## 2. Image Enhancement: Retinex

For scenarios like nights and underground garages, direct recognition often fails. We introduced the **Multi-Scale Retinex (MSR)** algorithm.
- **Principle**: Decomposes the image into reflection components (object properties) and illumination components (lighting), removing lighting effects to restore true object color.
- **Optimization**: Parallel acceleration optimization for GPU, controlling enhancement latency within **20ms**.

## 3. Character Recognition: LPRNet

Lightweight end-to-end license plate recognition network.
- **No Character Segmentation**: Directly predicts sequences for the whole license plate.
- **Lightweight & Efficient**: Extremely small model parameter size, ultra-fast inference speed.
- **Multi-Style Support**: Covers Blue plates, Yellow plates (Single/Double), Green plates (New Energy), White plates (Police), and other styles.
