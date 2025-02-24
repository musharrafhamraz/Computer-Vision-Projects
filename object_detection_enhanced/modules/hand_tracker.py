import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

    def track_hands(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                return self._get_hand_position(hand_landmarks, frame.shape)
        return None

    def _get_hand_position(self, landmarks, frame_shape):
        h, w = frame_shape[:2]
        # Access x and y attributes directly from NormalizedLandmark
        landmark = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        x, y = landmark.x, landmark.y
        return int(x * w), int(y * h)

    def close(self):
        self.hands.close()