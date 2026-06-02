from fastapi import FastAPI, HTTPException, Request, Query
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

app = FastAPI(title="Smart Campus — Analytics Service Backend", version="1.0.0")

reports_db = {}
anomalies_db = [
    {
        "id": "anom-001",
        "type": "HIGH_TEMPERATURE",
        "source": "sensor.iot",
        "description": "Nhiệt độ phòng máy vượt ngưỡng 40 độ C",
        "timestamp": "2026-05-26T10:00:00Z"
    }
]

class ReportRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    report_type: str = Field(..., description="Loại báo cáo: iot, camera, access")

class SensorEvent(BaseModel):
    eventType: str
    eventId: str
    deviceId: str
    timestamp: datetime

def verify_token(authorization: Optional[str]):
    if not authorization:
        raise HTTPException(status_code=401, detail="Thiếu Bearer token")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token không đúng định dạng Bearer")
    token = authorization.split(" ")[1]
    if token not in ["lab-token", "local-dev-token"]:
        raise HTTPException(status_code=403, detail="Token không hợp lệ hoặc hết hạn")
    return token

@app.get("/health")
def get_health():
    return {
        "status": "healthy",
        "service": "analytics-service",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/api/v1/analytics/summary")
def get_dashboard_summary(request: Request):
    verify_token(request.headers.get("authorization"))
    return {
        "total_records": 15420,
        "system_efficiency": 94.5,
        "active_sources": ["iot", "access_gate", "camera"],
        "last_updated": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/api/v1/analytics/reports", status_code=201)
def create_async_report(payload: ReportRequest, request: Request):
    # FastAPI sẽ tự động kiểm tra payload và quăng lỗi 422 trước khi chạy dòng lệnh dưới đây
    verify_token(request.headers.get("authorization"))
    
    if payload.report_type not in ["iot", "camera", "access"]:
        raise HTTPException(status_code=422, detail="report_type phải thuộc [iot, camera, access]")
    
    report_id = str(uuid.uuid4())
    reports_db[report_id] = {"status": "pending", "type": payload.report_type}
    return {"report_id": report_id, "status": "pending"}

@app.get("/api/v1/analytics/anomalies")
def get_anomalies(
    request: Request,
    page: int = Query(1, description="Số trang"), 
    limit: int = Query(20, description="Số bản ghi trên mỗi trang")
):
    # Kiểm tra phân trang âm trước (Trả về 400 theo đúng Postman test)
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page và Limit phải lớn hơn 0")
    
    verify_token(request.headers.get("authorization"))
    return {
        "page": page,
        "limit": limit,
        "total_items": len(anomalies_db),
        "items": anomalies_db
    }

@app.post("/api/v1/analytics/ingest/iot", status_code=202)
def ingest_iot_event(event: SensorEvent):
    return {"eventId": event.eventId, "acceptedAt": datetime.utcnow().isoformat() + "Z"}

@app.post("/api/v1/analytics/ingest/access", status_code=202)
def ingest_access_event(event: SensorEvent):
    return {"eventId": event.eventId, "acceptedAt": datetime.utcnow().isoformat() + "Z"}