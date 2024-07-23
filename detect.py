import cv2
from ultralytics import YOLO
import requests


def download_video(url, output_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print(f"Failed to download video. Status code: {response.status_code}")


def detect_objects(input_video, output_video):
    model = YOLO("yolov8n.pt")  # Load YOLOv8 model
    cap = cv2.VideoCapture(input_video)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        for result in results[0].boxes:
            x1, y1, x2, y2 = result.xyxy[0]
            conf = result.conf[0]
            cls = result.cls[0]
            label = f'{model.names[int(cls)]} {conf:.2f}'
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        out.write(frame)

    cap.release()
    out.release()
if __name__ == "__main__":
    video_url = "https://www.holidayinfo.cz/hol3_data.php?type=camvideo&ext=mp4&camid=2131&cdt=20240723120000&dt=20240723120000"
    input_video = "input.mp4"
    output_video = "output.mp4"
    download_video(video_url, input_video)
    detect_objects(input_video, output_video)
