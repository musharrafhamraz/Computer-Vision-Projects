import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, static_image_mode=False, max_num_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.draw_utils = mp.solutions.drawing_utils
        # Ensure values are properly cast to float
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=float(detection_confidence),
            min_tracking_confidence=float(tracking_confidence)
        )

    def find_hands(self, image, draw=True):
        """Processes the image and finds hand landmarks."""
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        processed_image = self.hands.process(rgb_image)
        if processed_image.multi_hand_landmarks:
            for hand_landmarks in processed_image.multi_hand_landmarks:
                if draw:
                    self.draw_utils.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            return processed_image.multi_hand_landmarks
        return None

    def get_landmark_positions(self, image, hand_landmarks, ids=[4, 8]):
        """Get specific landmark positions for the given hand."""
        height, width, _ = image.shape
        positions = {}

        # Iterate through specific landmark IDs
        for idx in ids:
            if 0 <= idx < len(hand_landmarks.landmark):  # Ensure index is valid
                x = int(hand_landmarks.landmark[idx].x * width)
                y = int(hand_landmarks.landmark[idx].y * height)
                positions[idx] = (x, y)
        return positions

