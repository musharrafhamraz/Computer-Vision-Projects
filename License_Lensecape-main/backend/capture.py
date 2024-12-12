import cv2
import argparse

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='yolov8 live.')
    parser.add_argument(
        "--webcam-resolution", 
        default=[640, 640], 
        nargs=2, 
        type=int)
    parser.add_argument(
        "--camera-index",
        default=0,
        type=int,
        help="Index of the camera to use (default is 0)."
    )
    args = parser.parse_args()
    return args

def start_capture(webcam_resolution, camera_index):
    frame_width, frame_height = webcam_resolution

    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    return cap

# import cv2
# import argparse

# def parse_arguments() -> argparse.Namespace:
#     parser = argparse.ArgumentParser(description='yolov8 live.')
#     parser.add_argument(
#         "--webcam-resolution", 
#         default=[640, 640], 
#         nargs=2, 
#         type=int)
#     parser.add_argument(
#         "--camera-id",
#         default=0,
#         type=int,
#         help="Camera ID (0 for default camera, 1 for the second camera, and so on)")
#     args = parser.parse_args()
#     return args

# def start_capture(webcam_resolution, camera_id=0):
#     frame_width, frame_height = webcam_resolution

#     cap = cv2.VideoCapture(camera_id)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

#     return cap


# import cv2
# import argparse

# def parse_arguments() -> argparse.Namespace:
#     parser = argparse.ArgumentParser(description='yolov8 live.')
#     parser.add_argument(
#         "--webcam-resolution", 
#         default=[1380, 720], 
#         nargs=2, 
#         type=int)
#     args = parser.parse_args()
#     return args

# def start_capture(webcam_resolution):
#     frame_width, frame_height = webcam_resolution

#     cap = cv2.VideoCapture(0)  # open the default camera
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

#     return cap
