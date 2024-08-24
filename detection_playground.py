from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Load YOLOv8 model
model_name = "best.pt"
#model_name = r"C:\projects\plovarna\repo\yolov8x.pt"
model_name = r"C:\projects\plovarna_1\repo\plovarna\best_e15_1280.pt"
model_name = r'c:\Users\martin\Downloads\best (1).pt'
model = YOLO(model_name)

# Load the image
img_p = r"C:\projects\plovarna_1\repo\plovarna\valimg\webcam_stream_20240701130000_90.png"
img_p = r'C:\projects\plovarna_1\repo\plovarna\valimg\webcam_stream_20240701130000_565.png'
frame = cv2.imread(img_p)

frame = frame[226:,:450,:]
frame.shape

# Run the model on the image
confidence_threshold = 0.1
results = model(frame, conf=confidence_threshold, verbose=True)
results = model.predict(frame,conf=confidence_threshold,verbose=True, imgsz=1280)

# Process the results
people_count = 0
for result in results[0].boxes:
    x1, y1, x2, y2 = result.xyxy[0]
    conf = result.conf[0]
    cls = result.cls[0]
    label = f'{model.names[int(cls)]} {conf:.2f}'
    if model.names[int(cls)] == "person":
        people_count += 1
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Convert BGR image (OpenCV) to RGB (Matplotlib)
frame_rgb_best = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Display the image with matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(frame_rgb_best)
plt.title(f'People count: {people_count}')
plt.axis('off')
plt.show()


#### Slicer 2

import cv2
import matplotlib.pyplot as plt
import supervision as sv
import numpy as np


# Define the callback function for InferenceSlicer
def callback(image_slice: np.ndarray) -> sv.Detections:
    results = model(image_slice)[0]  # Run inference on the slice

    # Extracting bounding boxes, class IDs, and confidence scores
    boxes = results.boxes.xyxy.cpu().numpy()
    class_ids = results.boxes.cls.cpu().numpy().astype(int)
    confidences = results.boxes.conf.cpu().numpy()

    # Create a Detections object
    detections = sv.Detections(
        xyxy=boxes,
        confidence=confidences,
        class_id=class_ids
    )

    return detections

# Initialize InferenceSlicer with the callback
slicer = sv.InferenceSlicer(callback=callback, slice_wh=(160, 160))

# Perform inference on the entire image
frame = cv2.imread(img_p)
detections = slicer(frame)

annotated_frame = sv.BoxAnnotator().annotate(
    scene=frame.copy(),
    detections=detections
)

# Convert BGR image (OpenCV) to RGB (Matplotlib)
annotated_image_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

# Display the image with matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(annotated_image_rgb)
plt.axis('off')
plt.show()

# Display the image with matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(frame_rgb_best)
plt.axis('off')
plt.show()



## SLicer 1
import cv2
import numpy as np
import supervision as sv
from inference import get_model
model = get_model(model_id="yolov8x-seg-640")
img_p = r"F:\plovarna\yolo_data\images\train\webcam_stream_20240701180000_917.png"
image = cv2.imread(img_p)

def callback(image_slice: np.ndarray) -> sv.Detections:
    results = model.infer(image_slice)[0]
    return sv.Detections.from_inference(results)

slicer = sv.InferenceSlicer(callback = callback, slice_wh=(320, 320))
detections = slicer(image)

mask_annotator = sv.MaskAnnotator()
label_annotator = sv.LabelAnnotator()

annotated_image = mask_annotator.annotate(
    scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)

plt.figure(figsize=(10, 10))
plt.imshow(annotated_image)
plt.axis('off')
plt.show()

## Slice 3
import cv2
import supervision as sv
from ultralytics import YOLO

image = cv2.imread(img_p)
# Load YOLOv8 model
model_name = "best.pt"
model = YOLO(model_name)


def callback(image_slice: np.ndarray) -> sv.Detections:
    result = model(image_slice)[0]
    return sv.Detections.from_ultralytics(result)


slicer = sv.InferenceSlicer(callback=callback, slice_wh=(320, 320), overlap_ratio_wh=(0.8, 0.8), iou_threshold=0.1)

detections = slicer(image)

annotated_frame = sv.BoxAnnotator().annotate(
    scene=frame.copy(),
    detections=detections
)

# Convert BGR image (OpenCV) to RGB (Matplotlib)
annotated_image_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

# Display the image with matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(annotated_image_rgb)
plt.axis('off')
plt.show()

# Display the image with matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(frame_rgb_best)
plt.axis('off')
plt.show()