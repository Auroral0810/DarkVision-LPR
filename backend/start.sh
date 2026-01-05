#!/bin/bash

# 激活 conda 环境并启动 FastAPI 服务
cd "$(dirname "$0")"

echo "正在启动 DarkVision-LPR 后端服务..."
echo "使用 conda 环境: DarkVision"
echo "端口: 8000"
echo ""

conda run -n DarkVision uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

