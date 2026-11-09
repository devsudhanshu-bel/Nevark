# Health Check API

## 1. Overview

The Health Check API provides a lightweight endpoint for checking the availability of the Nevark AI Backend.

It allows clients and external monitoring systems to send an HTTP GET request and receive a response indicating that the backend service is online.

Unlike the chat endpoint, this route does not invoke an AI model, access a database, or perform additional service operations.

## 2. Source File Details

| Property | Description |
|---|---|
| Module | Health Check API |
| File | `app/api/routes/health.py` |
| Framework | FastAPI |
| HTTP method | GET |
| Route prefix | `/health` |
| Endpoint | `/` |
| Router tag | `Health` |

## 3. Import Dependency

```python
from fastapi import APIRouter
```

`APIRouter` is used to define and organize the health-check endpoint independently from the other backend routes.

## 4. Router Initialization

```python
router = APIRouter(
    prefix="/health",
    tags=["Health"]
)
```

The router defines:

- `prefix="/health"` – Establishes the URL prefix for the health endpoint.
- `tags=["Health"]` – Groups the endpoint under the Health category in FastAPI's API documentation.

## 5. Health Check Endpoint

### Route: `GET /`

```python
@router.get("/")
async def health_check():
```

The endpoint is asynchronous and does not require any request parameters or request body.

Because the router has the `/health` prefix, its combined endpoint path is:

```http
GET /health/
```

### Processing

When a client sends a GET request:

1. FastAPI receives the request.
2. The `health_check()` function executes.
3. The function returns a predefined JSON response.

No additional processing is performed.

## 6. Response Structure

The endpoint returns:

```json
{
    "status": "online",
    "service": "Nevark AI Backend"
}
```

### Response Fields

| Field | Value | Description |
|---|---|---|
| `status` | `online` | Indicates that the endpoint responded |
| `service` | `Nevark AI Backend` | Identifies the backend service |

## 7. API Usage

### Request

```http
GET /health/
```

No authentication parameters, query parameters, or request body are declared in this route.

### Expected Response

```json
{
    "status": "online",
    "service": "Nevark AI Backend"
}
```

## 8. Integration with the Backend

The health router is registered in the central API router:

```python
api_router.include_router(health_router)
```

The routing structure is:

```text
FastAPI Application
       |
       v
   api_router
       |
       v
  health_router
       |
       v
 GET /health/
       |
       v
 health_check()
       |
       v
 JSON Response
```

## 9. Important Implementation Notes

- The endpoint is designed as a lightweight availability check.
- It does not invoke the chat service or other business logic.
- It does not perform database connectivity checks.
- It does not verify external API availability.
- It does not inspect vector-store availability.
- It does not perform authentication or authorization.
- It returns a predefined response whenever the endpoint executes successfully.

**Important:** The `online` status confirms that the health-check endpoint responded. It does not independently establish that every backend dependency is operational.

## 10. Conclusion

The Health Check API provides a simple interface for checking whether the Nevark AI Backend is responding.

Its minimal implementation makes it suitable as a basic service availability endpoint for clients, development environments, and monitoring integrations.