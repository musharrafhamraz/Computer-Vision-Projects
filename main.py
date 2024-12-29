import cv2
import numpy as np

def detect_shirt_keypoints_from_camera():
    # Load pre-trained human detection model (MobileNet SSD)
    net = cv2.dnn.readNetFromCaffe(
        "deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel"
    )

    # Initialize camera feed
    cap = cv2.VideoCapture(0)  # 0 for default camera
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    print("Press 'q' to quit.")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from the camera.")
            break

        # Prepare the frame for human detection
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()

        # Loop through detections to find the largest human (torso region)
        shirt_region = None
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.6:  # Confidence threshold
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Assume the torso is the lower half of the detected box
                torso_startY = startY + (endY - startY) // 3
                shirt_region = frame[torso_startY:endY, startX:endX]

                # Process the shirt region if it exists
                if shirt_region is not None and shirt_region.size > 0:
                    # Convert the shirt region to grayscale
                    gray_shirt_region = cv2.cvtColor(shirt_region, cv2.COLOR_BGR2GRAY)

                    # Detect keypoints and compute descriptors in the shirt region
                    keypoints, descriptors = sift.detectAndCompute(gray_shirt_region, None)

                    # Draw keypoints on the shirt region
                    shirt_with_keypoints = cv2.drawKeypoints(
                        shirt_region, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
                    )

                    # Replace the shirt region in the frame with the processed region
                    frame[torso_startY:endY, startX:endX] = shirt_with_keypoints

        # Display the frame with keypoints
        cv2.imshow("Detected Keypoints on Shirt", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Run the real-time detection
detect_shirt_keypoints_from_camera()
