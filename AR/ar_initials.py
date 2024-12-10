import cv2
import numpy as np

# Load the marker image (reference image)
marker_image = cv2.imread("marker.jpg", cv2.IMREAD_GRAYSCALE)

# Initialize the ORB detector
orb = cv2.ORB_create()

# Compute keypoints and descriptors for the marker image
keypoints_marker, descriptors_marker = orb.detectAndCompute(marker_image, None)

# Initialize the video capture (webcam)
cap = cv2.VideoCapture(0)

# Define the virtual content (an image to overlay)
virtual_content = cv2.imread("virtual_content.jpg")

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect keypoints and descriptors in the current frame
    keypoints_frame, descriptors_frame = orb.detectAndCompute(gray_frame, None)

    # Use BFMatcher to find matches between descriptors
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors_marker, descriptors_frame)

    # Sort matches by distance (best matches first)
    matches = sorted(matches, key=lambda x: x.distance)

    # Define a threshold for good matches
    if len(matches) > 10:
        # Extract the matched keypoints
        src_points = np.float32([keypoints_marker[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_points = np.float32([keypoints_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        # Compute the homography matrix
        matrix, mask = cv2.findHomography(src_points, dst_points, cv2.RANSAC, 5.0)

        # Get the dimensions of the marker image
        h, w = marker_image.shape

        # Define the marker corners
        marker_corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)

        # Transform the marker corners to the video frame
        transformed_corners = cv2.perspectiveTransform(marker_corners, matrix)

        # Draw the transformed corners on the frame
        frame = cv2.polylines(frame, [np.int32(transformed_corners)], True, (0, 255, 0), 3)

        # Warp the virtual content to align with the marker
        h_frame, w_frame, _ = frame.shape
        virtual_warped = cv2.warpPerspective(virtual_content, matrix, (w_frame, h_frame))

        # Create a mask for blending the virtual content
        mask = cv2.fillConvexPoly(np.zeros_like(frame), np.int32(transformed_corners), (255, 255, 255))

        # Blend the virtual content into the frame
        frame = cv2.bitwise_and(frame, cv2.bitwise_not(mask))
        frame = cv2.add(frame, virtual_warped)

    # Display the AR result
    cv2.imshow("AR Application", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
