# License Lensecape

This is a comprehensive guide for setting up and using the License Lensecape, a real-time vehicle monitoring application that performs object detection and optical character recognition (OCR) on license plates. The system uses the YOLO (You Only Look Once) model for object detection and EasyOCR for optical character recognition. Detected vehicles and their license plates are logged in an Excel file for later analysis.

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Run the Application

To start the surveillance system, run the `Main.py` script:

```bash
python Main.py
```

The application will start a Flask server, and you can access the video feed and logged data through the provided API endpoints.

### 2. API Endpoints

#### Video Feed

- Video feed for Camera 1: [http://localhost:5000/api/video_feed_cam1](http://localhost:5000/api/video_feed_cam1)

This endpoint provides a real-time video feed of Camera 1, with detected objects and license plate annotations.

#### Excel Data

- Retrieve Excel data: [http://localhost:5000/api/get_excel_data](http://localhost:5000/api/get_excel_data)

This endpoint returns the logged data in the form of a JSON response, containing timestamped information about detected license plates.

## Main Functions

### 1. `setup_workbook`

```python
def setup_workbook():
    try:
        LOG_FILE_PATH = 'vehicle_logs.xlsx'
        workbook = openpyxl.load_workbook(LOG_FILE_PATH)
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["Timestamp", "Plate Number", "Class ID", "Confidence"])

    return workbook.active
```

This function initializes or loads an Excel workbook for logging information about detected license plates. If the workbook does not exist, a new one is created with the required headers.

### 2. `read_logs`

```python
def read_logs(sheet):
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        timestamp, plate_number, class_id, confidence = row
        data.append({
            "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "Plate Number": plate_number,
            "Class ID": class_id,
            "Confidence": confidence
        })
    return data
```

This function reads the logged data from the provided Excel sheet and formats it into a list of dictionaries containing timestamp, plate number, class ID, and confidence.

### 3. `save_log`

```python
def save_log(log_data, sheet):
    timestamp, plate_number, class_id, confidence = log_data
    plate_number = ''.join(char for char in plate_number if char.isprintable())
    sheet.append([timestamp, plate_number, class_id, confidence])
```

This function appends a new log entry to the Excel sheet, including timestamp, plate number, class ID, and confidence. It ensures that non-printable characters in the plate number are filtered out.

### 4. `generate_frames`

```python
def generate_frames(cap, model, reader, save_folder, sheet):
    # ... (frame_interval, frame_count initialization)

    while True:
        ret, frame = cap.read()

        if frame_count % frame_interval == 0:
            # ... (perform object detection)

            frame = annotate_frame(frame, detections, labels)
            ret, jpeg = cv2.imencode('.jpg', frame)

            if not ret:
                continue

            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

        frame_count += 1
```

This function continuously generates frames from the video capture, performs object detection, and annotates the frames with bounding boxes and labels. It yields the annotated frames as a continuous video feed in JPEG format.

### 5. `video_feed_cam1`

```python
@app.route('/api/video_feed_cam1')
def video_feed_cam1():
    print("Request received for /api/video_feed_cam1")
    return Response(generate_frames(cap, model, reader, save_folder, sheet),
                    mimetype='video/mp4',
                    content_type='multipart/x-mixed-replace; boundary=frame')
```

This function is the Flask route for providing the video feed of Camera 1. It utilizes the `generate_frames` function and returns the video feed as a response with the appropriate MIME type.

### 6. `start_capture`

```python
def start_capture(webcam_resolution, camera_index):
    frame_width, frame_height = webcam_resolution

    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    return cap
```

This function initializes and configures the video capture using OpenCV, setting the frame width and height according to the specified webcam resolution.

### 7. `initialize_easyocr`

```python
def initialize_easyocr():
    return easyocr.Reader(['en'])
```

This function initializes the EasyOCR reader with English language support.

### 8. `perform_ocr`

```python
def perform_ocr(reader, image_path):
    try:
        results = reader.readtext(image_path)

        recognized_text = ""
        for detection in results:
            text = detection[1]
            text = ''.join(char for char in text if char.isalnum())
            recognized_text += text

        return recognized_text
    except Exception as e:
        print("OCR operation failed with an error:", e)
        return ""
```

This function performs optical character recognition (OCR) on a given image using the EasyOCR reader. It processes the OCR results and extracts alphanumeric characters from the detected text.

### 9. `save_cropped_image`

```python
def save_cropped_image(plate_image, save_folder, timestamp):
    image_name = f"{save_folder}/plate_{timestamp}.jpg"
    cv2.imwrite(image_name, plate_image)
    return image_name
```

This function saves a cropped license plate image to the specified folder with a filename based on the timestamp.

### 10. `initialize_yolo_model`

```python
def initialize_yolo_model(model_path):
    return YOLO(model_path)
```

This function initializes the YOLO (You Only Look Once) model for object detection using the Ultralytics YOLO library.

### 11. `perform_object_detection`

```python
def perform_object_detection(model, frame):
    return model(frame)[0]
```

This function performs object detection on a given video frame using the YOLO model and returns the detection results.

### 12. `annotate_frame`

```python
def annotate_frame(frame, detections, labels):
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
    return box_annotator.annotate(scene=frame, detections=detections, labels=labels)
```

This function annotates a video frame with bounding boxes and labels based on object detection results. It uses the `

BoxAnnotator` class from the `supervision` module.

## Dependencies

- Flask
- Flask-RESTful
- OpenCV
- Openpyxl
- Ultralytics YOLO
- EasyOCR

Make sure to have these dependencies installed before running the application.

## Notes

- The application assumes a webcam is available at the specified camera index.
- The YOLO model file is expected to be at the specified path.
- Ensure proper camera access permissions and webcam functionality.
- The Excel workbook is used to log timestamped information about detected license plates.

Feel free to customize and extend the system based on your requirements!