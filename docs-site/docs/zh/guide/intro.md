# 项目介绍

![DarkVision Badge](https://img.shields.io/badge/DarkVision-LPR-blue?style=flat-square&logo=visual-studio-code)
![Version](https://img.shields.io/badge/Version-v2.0.0-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-orange?style=flat-square)

::: info 简介
**DarkVision-LPR** 是一款专为**低光照环境**设计的高精度车牌识别系统。
:::

针对夜间、地下车库、隧道等复杂光线场景，我们采用了 **YOLOv11m** 深度学习模型，并结合 **Retinex 图像增强算法**，在 CCPD2019 和 CCPD2020 数据集上通过 **3万张** 图像进行了充分训练，模型准确率高达 **99.9%**。

## 项目背景

在智能交通系统中，车牌识别（LPR）是一项关键技术。然而，传统的 LPR 系统在低光照条件下往往表现不佳，容易出现漏检或误检。为了解决这一痛点，DeepVision 团队开发了 **DarkVision-LPR**，旨在为极端光线环境提供可靠的识别能力。

## 核心特性

- 🌑 **夜视增强**：自适应图像增强算法 (Retinex)，让极暗环境下的车牌也清晰可见。
- ⚡ **毫秒级识别**：基于高性能 YOLOv11m (Medium) 模型，实现实时流媒体检测。
- 📊 **数据洞察**：内置强大的数据分析大屏，实时监控识别流量、车型分布及 KPI 指标。
- 🌐 **全栈生态**：包含用户门户、管理后台及官方宣传网站，满足不同角色需求。
- 🔒 **企业级安全**：支持实名认证、JWT 鉴权及操作日志审计。

## 适用场景

- 🏙️ **城市安防**：夜间道路监控、卡口抓拍。
- 🅿️ **智慧停车**：地下停车场、光线不足的立体车库。
- 🛣️ **高速收费**：隧道出入口、恶劣天气下的车辆识别。
