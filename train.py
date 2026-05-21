from ultralytics import YOLO

def train_model():
    model = YOLO("models/yolov8n.pt")
    model.train(
        data="dataset/data.yaml",
        epochs=10,
        imgsz=640,
        batch=8,
        device="cpu",       # change to 0 if you have NVIDIA GPU
        patience=10,
        save=True,
        project="runs/detect",
        name="pothole_v1"
    )
    print("\nDone! Now run:")
    print("copy runs\\detect\\pothole_v1\\weights\\best.pt models\\best.pt")

if __name__ == "__main__":
    train_model()