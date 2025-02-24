from modules.hand_tracker import HandTracker
from modules.object_detector import ObjectDetector
from modules.llm_enhancer import LLMEnhancer
from modules.display import Display
import cv2

def main():
    # Initialize components
    hand_tracker = HandTracker()
    object_detector = ObjectDetector()
    llm_enhancer = LLMEnhancer()
    display = Display()

    # Start video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Optional: Lower resolution for speed
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_skip = 2  # Process every 2nd frame
    frame_count = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            frame_count += 1
            if frame_count % frame_skip != 0:
                continue  # Skip this frame

            # Track hand
            hand_pos = hand_tracker.track_hands(frame)

            # Detect objects near hand
            detected_objects = object_detector.detect_objects(frame, hand_pos)

            # Enhance response with LLM
            text = llm_enhancer.enhance_response(detected_objects[0] if detected_objects else None)

            # Display result
            display.show_frame(frame, text)

            # Exit on 'q'
            if display.wait_key() == ord('q'):
                break

    finally:
        cap.release()
        hand_tracker.close()
        display.close()

if __name__ == "__main__":
    main()