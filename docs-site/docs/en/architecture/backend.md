# Backend Architecture

The backend services are built on the **Python** ecosystem, fully leveraging its advantages in the AI field to achieve seamless integration of business logic and model inference.

## Technology Stack

| Technology | Choice | Role |
| :--- | :--- | :--- |
| **Web Framework** | FastAPI | High-performance asynchronous ASGI framework, auto-generating docs |
| **Language Version** | Python 3.10+ | Utilizing the latest async features and type hinting |
| **Server** | Uvicorn | Production-grade ASGI server implementation |
| **ORM** | SQLAlchemy 2.0 | Modern asynchronous database mapping tool |
| **Data Validation** | Pydantic 2.0 | Powerful data parsing and validation library |
| **Authentication** | PyJWT (OAuth2) | Standardized stateless identity verification |
| **DB Migration** | Alembic | Versioned database schema change management |
| **Task Queue** | Celery / Redis Queue | Handling time-consuming tasks (e.g., video analysis) |

## Core Modules

### 1. API Interface Module (app/api)
Follows RESTful specifications, providing versioned interface services (`/api/v1/...`).
- **Deps**: Unified dependency injection system (DB session, current user, permission validation).

### 2. Business Service Layer (app/services)
Encapsulates specific business logic to avoid bloated Controller layers.
- `RecognitionService`: Handles recognition flow, calling the inference engine.
- `AuthService`: Handles login, registration, token refresh.
- `AnalysisService`: Handles data report aggregation calculations.

### 3. Real-time Communication
Utilizes FastAPI's **WebSocket** support to achieve full-duplex real-time push of recognition progress.
- Status Flow: `Uploading` -> `Detecting` -> `Enhancing` -> `Recognizing` -> `Completed`

## Performance Optimization
- **Async I/O**: Uses `async/await` throughout for I/O-intensive operations (Database, Network requests).
- **Connection Pool**: Database and Redis are configured with connection pools to reuse connection resources.
- **Caching Strategy**: Uses Redis caching for high-frequency read data that rarely changes (e.g., configuration, user info).
