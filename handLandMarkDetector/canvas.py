# import cv2
# import mediapipe as mp
# import numpy as np

# class HandTracker:
#     def __init__(self, maxHands=1, detectionCon=0.7, trackCon=0.7):
#         self.maxHands = maxHands
#         self.detectionCon = detectionCon
#         self.trackCon = trackCon

#         self.mpHands = mp.solutions.hands
#         self.hands = self.mpHands.Hands(max_num_hands=self.maxHands, min_detection_confidence=self.detectionCon,
#                                         min_tracking_confidence=self.trackCon)
#         self.mpDraw = mp.solutions.drawing_utils

#     def findHands(self, img, draw=True):
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         self.results = self.hands.process(imgRGB)
#         if draw and self.results.multi_hand_landmarks:
#             for handLms in self.results.multi_hand_landmarks:
#                 self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
#         return img

#     def findPosition(self, img, handNo=0):
#         lmList = []
#         if self.results.multi_hand_landmarks:
#             myHand = self.results.multi_hand_landmarks[handNo]
#             for id, lm in enumerate(myHand.landmark):
#                 h, w, _ = img.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#                 lmList.append((id, cx, cy))
#         return lmList

# def fingers_up(lmList):
#     """Detects which fingers are up based on landmarks."""
#     if len(lmList) < 20:
#         return []
#     fingers = []
#     tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
#     for tip in tips:
#         fingers.append(lmList[tip][2] < lmList[tip - 2][2])  # Y-coordinates check
#     return fingers

# def main():
#     cap = cv2.VideoCapture(0)
#     cap.set(3, 1280)  # Set width to 1280
#     cap.set(4, 720)   # Set height to 720
#     tracker = HandTracker()
#     canvas = None
#     color_index = 0
#     colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]
#     thickness = 5
#     prev_x, prev_y = 0, 0
#     font_size = 1

#     while True:
#         success, img = cap.read()
#         img = cv2.flip(img, 1)
#         h, w, _ = img.shape
#         if canvas is None:
#             canvas = np.zeros((h, w, 3), np.uint8)

#         img = tracker.findHands(img)
#         lmList = tracker.findPosition(img)

#         # Initialize finger_state
#         finger_state = [False, False, False, False]

#         if len(lmList) != 0:
#             x, y = lmList[8][1], lmList[8][2]  # Index fingertip coordinates
#             finger_state = fingers_up(lmList)

#             # Draw mode (only index finger up)
#             if finger_state[0] and not finger_state[1]:  # Index finger up
#                 if prev_x == 0 and prev_y == 0:
#                     prev_x, prev_y = x, y
#                 cv2.line(canvas, (prev_x, prev_y), (x, y), colors[color_index], thickness)
#                 prev_x, prev_y = x, y

#             # Color change mode (index and middle fingers together)
#             elif finger_state[0] and finger_state[1]:  # Index and middle fingers up
#                 color_index = (color_index + 1) % len(colors)
#                 prev_x, prev_y = x, y

#             # Reset positions when no fingers or other gestures are detected
#             else:
#                 prev_x, prev_y = 0, 0

#         # Combine the canvas and the webcam feed
#         img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
#         _, img_inverted = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
#         img_inverted = cv2.cvtColor(img_inverted, cv2.COLOR_GRAY2BGR)
#         img = cv2.bitwise_and(img, img_inverted)
#         img = cv2.bitwise_or(img, canvas)

#         # Draw color palette on the right side
#         palette_x = w - 100
#         for i, color in enumerate(colors):
#             cv2.rectangle(img, (palette_x, 30 + i * 40), (palette_x + 60, 30 + (i + 1) * 40), color, -1)
#             cv2.putText(img, f'Color {i + 1}', (palette_x + 70, 30 + (i + 1) * 40 - 10), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

#         # Draw buttons for increasing and decreasing thickness
#         cv2.rectangle(img, (20, 20), (80, 80), (100, 100, 100), -1)  # Increase thickness button
#         cv2.putText(img, 'Increase', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), 2)
#         cv2.rectangle(img, (20, 100), (80, 160), (100, 100, 100), -1)  # Decrease thickness button
#         cv2.putText(img, 'Decrease', (30, 130), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), 2)

#         # Display thickness and color information
#         cv2.putText(img, f'Thickness: {thickness}', (10, h - 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), 2)
#         cv2.putText(img, f'Selected Color: {color_index + 1}', (10, h - 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), 2)

#         cv2.imshow("Air Canvas", img)

#         # Check for button presses to change thickness
#         if finger_state[0] and finger_state[1]:
#             # Increase thickness button
#             if prev_y < 80:
#                 thickness = min(thickness + 1, 20)
#             # Decrease thickness button
#             elif prev_y > 100:
#                 thickness = max(1, thickness - 1)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self, maxHands=1, detectionCon=0.7, trackCon=0.7):
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=self.maxHands, min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if draw and self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))
        return lmList

def fingers_up(lmList):
    """Detects which fingers are up based on landmarks."""
    if len(lmList) < 20:
        return []
    fingers = []
    tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
    for tip in tips:
        fingers.append(lmList[tip][2] < lmList[tip - 2][2])  # Y-coordinates check
    return fingers

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280) 
    cap.set(4, 720)   
    tracker = HandTracker()
    canvas = None
    color_index = 0
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]
    thickness = 5
    prev_x, prev_y = -1, -1
    eraser_mode = False

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        if canvas is None:
            canvas = np.zeros((h, w, 3), np.uint8)

        img = tracker.findHands(img)
        lmList = tracker.findPosition(img)

        # Initialize finger_state
        finger_state = [False, False, False, False]

        if len(lmList) != 0:
            x, y = lmList[8][1], lmList[8][2]  # Index fingertip coordinates
            finger_state = fingers_up(lmList)

            # Draw mode (only index finger up)
            if finger_state[0] and not finger_state[1]:  # Index finger up
                if prev_x == -1 and prev_y == -1:  # If previous position is invalid
                    prev_x, prev_y = x, y
                if not eraser_mode:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), colors[color_index], thickness)
                prev_x, prev_y = x, y  # Update previous position

            # Color selection mode (index and middle fingers joined while hovering over a color)
            elif all(finger_state):
                    prev_x, prev_y = -1, -1
            elif finger_state[0] and finger_state[1]:  # Index and middle fingers up
                # Check if hovering over color palette
                if x > (w - 160) and x < (w - 40):  # Right side color palette area
                    color_index = (y // 40) % len(colors)  # Select color based on y position
                    prev_x, prev_y = -1, -1  # Reset previous position
            else:
                prev_x, prev_y = -1, -1  # Reset previous position

        # Combine the canvas and the webcam feed
        img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, img_inverted = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
        img_inverted = cv2.cvtColor(img_inverted, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, img_inverted)
        img = cv2.bitwise_or(img, canvas)

        # Draw color palette on the right side
        palette_x = w - 160
        for i, color in enumerate(colors):
            cv2.rectangle(img, (palette_x, 30 + i * 90), (palette_x + 120, 30 + (i + 1) * 90), color, -1)  # Make buttons bigger
            # cv2.putText(img, f'Color {i + 1}', (palette_x + 130, 30 + (i + 1) * 40 - 10),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Draw eraser button
        cv2.rectangle(img, (20, 180), (80, 240), (100, 100, 100), -1)  # Eraser button
        cv2.putText(img, 'Eraser', (30, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Display thickness and color information
        cv2.putText(img, f'Thickness: {thickness}', (10, h - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, f'Selected Color: {color_index + 1}', (10, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Air Canvas", img)

        # Check if eraser button is pressed
        if prev_x < 80 and prev_x > 20:
            if prev_y > 180:
                eraser_mode = not eraser_mode  # Toggle eraser mode

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
