# FAQ

## General

### What is DarkVision-LPR?
DarkVision-LPR is a license plate recognition system optimized for low-light environments. It uses the Retinex algorithm to enhance images before performing YOLOv11 and LPRNet inference, ensuring high recognition rates at night.

### Is it open source?
The Community Edition is open source for learning and exchange. The Pro and Enterprise editions are commercial closed-source software.

## Technical

### What are the hardware requirements?
- **CPU**: Minimal requirement is AVX2 support. Recommended to use Intel i5 10th Gen or above.
- **GPU**: Strongly recommended to use NVIDIA GPU (6GB+ VRAM) for acceleration, otherwise inference speed might be slow.
- **Memory**: 8GB+ (16GB recommended).

### How to deploy?
We recommend using Docker Compose for one-click deployment. Please refer to the [Quick Start](/en/guide/quick-start) guide.

### Why is the first recognition slow?
The deep learning model needs to be loaded into memory/VRAM on the first run, which takes some time (Cold Start). Subsequent requests will be millisecond-level.

## Troubleshooting

### "RuntimeError: CUDA out of memory"
Your GPU VRAM is insufficient. Try reducing the `batch_size` in the configuration or switching to the YOLOv11n (Nano) model, which is lighter.

### "Connection Refused"
Please check if the backend service (port 8000) and Database/Redis containers have started normally. You can use `docker logs` to view the logs.
