from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from core.detector import PotholeDetector
from app.database import (
    save_detection, get_all_detections,
    get_stats, update_status
)
import tempfile, os

router = APIRouter()
detector = PotholeDetector()


@router.post("/detect")
async def detect(
    image: UploadFile = File(...),
    lat: Optional[float] = Form(None),
    lng: Optional[float] = Form(None)
):
    """Upload an image → get pothole detections back."""
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    gps = (lat, lng) if lat and lng else None

    # Save upload to temp file
    suffix = os.path.splitext(image.filename)[-1] or ".jpg"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        contents = await image.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        detections = detector.detect(tmp_path, gps_coords=gps)
    finally:
        os.unlink(tmp_path)

    for d in detections:
        save_detection(d)

    return {
        "status": "success",
        "count": len(detections),
        "detections": detections
    }


@router.get("/detections")
def list_detections():
    """Get all saved detections."""
    return get_all_detections()


@router.get("/stats")
def stats():
    """Get summary statistics."""
    return get_stats()


@router.patch("/detections/{detection_id}/status")
def mark_status(detection_id: int, status: str):
    """Mark a pothole as fixed or pending."""
    if status not in ("pending", "fixed"):
        raise HTTPException(status_code=400, detail="Status must be 'pending' or 'fixed'")
    update_status(detection_id, status)
    return {"status": "updated", "id": detection_id}