# API Reference

DarkVision-LPR provides standard RESTful APIs for developers to integrate.

## Base URL
Since the default deployment port is 8000:
```
http://localhost:8000/api/v1
```

## Authentication
Most interfaces require a JWT Token.
1. Call `/login` to get `access_token`.
2. Add the header to subsequent requests: `Authorization: Bearer <your_token>`.

## Core Endpoints

### Recognition

`POST /recognition/tasks/`
- **Description**: Submit a recognition task (supports image file).
- **Body**: `multipart/form-data` -> `file`
- **Response**:
```json
{
  "plate_number": "苏A12345",
  "confidence": 0.99,
  "processing_time_ms": 150
}
```

### History

`GET /recognition/history/`
- **Query Params**: `page`, `size`, `start_date`, `end_date`, `plate_num`
- **Response**: Paginated recognition record list.

### Analysis

`GET /analysis/dashboard`
- **Description**: Get data for dashboard charts.
- **Response**: Includes `total_count`, `trend_data`, `distribution`, etc.

## Interactive Documentation (Swagger UI)

After starting the backend service, access the auto-generated interactive documentation:
- [http://localhost:8000/docs](http://localhost:8000/docs)
- [http://localhost:8000/redoc](http://localhost:8000/redoc)
