from ultralytics import YOLO
import cv2
import os
from datetime import datetime
from core.severity import classify_severity
from core.gps_tagger import get_gps_tag

class PotholeDetector:
    def __init__(self, model_path="models/best.pt", conf=0.4):
        self.model = YOLO(model_path)
        self.conf = conf
        os.makedirs("reports/images", exist_ok=True)

    def detect(self, source, gps_coords=None, save=True):
        results = self.model.predict(source=source, conf=self.conf, save=False)
        detections = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                severity = classify_severity(x1, y1, x2, y2)
                lat, lng = gps_coords if gps_coords else get_gps_tag()

                detection = {
                    "timestamp": datetime.now().isoformat(),
                    "confidence": round(confidence, 3),
                    "severity": severity,
                    "bbox": [x1, y1, x2, y2],
                    "lat": lat,
                    "lng": lng,
                    "image_path": ""
                }

                if save and hasattr(r, 'orig_img'):
                    img = r.orig_img.copy()
                    color = {
                        "small":  (0, 200, 0),
                        "medium": (0, 165, 255),
                        "large":  (0, 0, 220)
                    }[severity]
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                    label = f"{severity.upper()} {confidence:.2f}"
                    cv2.putText(img, label, (x1, y1 - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    fname = f"reports/images/{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
                    cv2.imwrite(fname, img)
                    detection["image_path"] = fname

                detections.append(detection)

        return detections