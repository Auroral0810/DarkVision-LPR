# Architecture Overview

DarkVision-LPR adopts a layered, decoupled **cloud-native microservices architecture** design. The overall system is divided into the Frontend Presentation Layer, Backend Business Layer, AI Inference Layer, and Data Storage Layer. Each module has clear responsibilities and communicates via standardized RESTful APIs and WebSockets, providing good horizontal scalability.

## System Architecture Diagram

![System Architecture Diagram](https://placehold.co/800x400?text=System+Architecture)

> (This is a schematic diagram; the actual architecture includes more detailed components)

## Core Layers

### 1. Frontend Presentation Layer
Responsible for user interaction and data visualization.
- **User Portal**: For end-users, providing recognition functions, history records, and personal center.
- **Admin Portal**: For administrators, providing user management, system monitoring, and content publishing.
- **Official Website**: Marketing and documentation display.

### 2. Backend Business Layer
High-performance asynchronous services built on **FastAPI**, handling core business logic.
- **Authentication (Auth)**: JWT authorization, RBAC permission control.
- **Business Logic**: Order processing, package management, quota control.
- **Task Scheduling**: Coordinates recognition tasks and distributes them to inference services.

### 3. AI Inference Layer
Independently deployed deep learning inference services, decoupling business from compute-intensive tasks.
- **YOLOv11m**: Responsible for vehicle detection and license plate localization.
- **LPRNet**: Responsible for license plate character recognition.
- **Retinex**: Responsible for low-light image enhancement.

### 4. Data Storage Layer
- **MySQL**: Stores user data, orders, and structured recognition records.
- **Redis**: Caches sessions, hot data, and message queues.
- **OSS (Object Storage)**: Sinks storage for original images and enhanced image resources.

## Design Principles

- **Frontend-Backend Separation**: Improves development efficiency and supports multi-terminal adaptation.
- **Service Decoupling**: Separation of business logic and AI inference, non-blocking.
- **High Availability**: Key components (e.g., Redis, Database) support cluster deployment.
- **Security**: Full-link data encryption, comprehensive permission auditing.
