# import cv2
# import mediapipe as mp
# import time

# # Combined element list and expanded compounds
# elements = ["H", "Na", "Bi", "Mg", "C", "Cl", "O", "Se", "Ca", "He", "S", "N"]
# compounds = {
#     ("H", "O"): "H₂O",
#     ("Na", "Cl"): "NaCl",
#     ("Mg", "O"): "MgO",
#     ("C", "O"): "CO₂",
#     ("H", "Cl"): "HCl",
#     ("Ca", "O"): "CaO",
#     ("Na", "O"): "Na₂O",
#     ("S", "O"): "SO₂",
#     ("N", "O"): "NO₂",
# }

# # Initialize Mediapipe for hand tracking
# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
# hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# # Variables to store selected elements and result
# selected_element1 = None
# selected_element2 = None
# result = None

# # Function to detect if fingers are close
# def is_close(hand_landmarks, img, threshold=30):
#     h, w, _ = img.shape
#     index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
#     middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

#     ix, iy = int(index_finger.x * w), int(index_finger.y * h)
#     mx, my = int(middle_finger.x * w), int(middle_finger.y * h)
#     distance = ((ix - mx) ** 2 + (iy - my) ** 2) ** 0.5
#     return distance < threshold

# # Function to check which element is selected based on hand y-position
# def get_selected_element(y):
#     box_height = 100  # Height of each element box
#     index = y // box_height
#     if 0 <= index < len(elements):
#         return elements[int(index)]
#     return None

# # Initialize camera and set resolution
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)

# pTime = 0  # To calculate FPS

# while True:
#     success, img = cap.read()
#     if not success:
#         break

#     # Convert to RGB for Mediapipe processing
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#      # Draw combined element sidebar on the left side in a 2x6 grid
#     num_columns = 2
#     num_rows = 6
#     element_width = 180  # Width of each element box
#     element_height = 100  # Height of each element box

#     for i, element in enumerate(elements):
#         row = i // num_columns
#         col = i % num_columns
#         x_position = 10 + col * element_width
#         y_position = 10 + row * element_height
#         cv2.rectangle(img, (x_position, y_position), (x_position + element_width, y_position + element_height), (255, 255, 255), 1)  # Draw only border
#         cv2.putText(img, element, (x_position + 30, y_position + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

#     # Draw combination result area
    
#     cv2.rectangle(img, (400, 10), (1220, 200), (0, 255, 0), 2)
#     if selected_element1:
#         cv2.putText(img, f"{selected_element1 } +", (420, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
#     if selected_element2:
#         cv2.putText(img, selected_element2, (590, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
#     if result:
#         cv2.putText(img, f"={result}", (650, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    
#     cv2.rectangle(img, (400, 230), (1220, 630), (0, 255, 0), 2)
#     cv2.putText(img, "hello this is description...", (420, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

#     # Process hand landmarks if detected
#     if results.multi_hand_landmarks:
#         for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
#             mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#             h, w, _ = img.shape
#             cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * h)

#             # Check if a close gesture is made
#             if is_close(hand_landmarks, img):
#                 selected_element = get_selected_element(cy)
#                 if selected_element1 is None:
#                     selected_element1 = selected_element
#                 elif selected_element2 is None and selected_element != selected_element1:  # Ensure the second is different
#                     selected_element2 = selected_element

#     # Combine selected elements when both are chosen
#     if selected_element1 and selected_element2:
#         result = compounds.get((selected_element1, selected_element2), "No Match")

#     # Display the "Clear" button below the equation boxclear

    
#     cv2.putText(img, "Press 'C' to clear", (400, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

#     # Check for "Clear" button press
#     if cv2.waitKey(1) & 0xFF == ord('c'):  # Press 'c' to clear selections
#         selected_element1 = None
#         selected_element2 = None
#         result = None

#     # Display FPS
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

#     # Show the final image
#     cv2.imshow("Compound Maker", img)

#     # Exit on 'q' press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2
import mediapipe as mp
import time

# Combined element list and expanded compounds
elements_first = ["O", "Se", "Ca", "He", "S", "N"]
elements_second = ["H", "Na", "Bi", "Mg", "C", "Cl"]
compounds = {
    ("H", "O"): "H₂O",
    ("Na", "Cl"): "NaCl",
    ("Mg", "O"): "MgO",
    ("C", "O"): "CO₂",
    ("H", "Cl"): "HCl",
    ("Ca", "O"): "CaO",
    ("Na", "O"): "Na₂O",
    ("S", "O"): "SO₂",
    ("N", "O"): "NO₂",
}

# Initialize Mediapipe for hand tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Variables to store selected elements and result
selected_element1 = None
selected_element2 = None
result = None
last_selection_time = 0  # To prevent rapid selections

# Function to detect if fingers are close
def is_close(hand_landmarks, img, threshold=30):
    h, w, _ = img.shape
    index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

    ix, iy = int(index_finger.x * w), int(index_finger.y * h)
    mx, my = int(middle_finger.x * w), int(middle_finger.y * h)
    distance = ((ix - mx) ** 2 + (iy - my) ** 2) ** 0.5
    return distance < threshold

# Function to check which element is selected based on hand y-position
def get_selected_element(y, elements):
    box_height = 100  # Height of each element box
    index = y // box_height
    if 0 <= index < len(elements):
        return elements[int(index)]
    return None

# Initialize camera and set resolution
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

pTime = 0  # To calculate FPS

while True:
    success, img = cap.read()
    if not success:
        break

    # Convert to RGB for Mediapipe processing
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Draw grid for elements
    for i, element in enumerate(elements_first):
        y_pos = i * 100 + 10
        cv2.rectangle(img, (950, y_pos), (1050, y_pos + 100), (200, 200, 200), cv2.FILLED)
        cv2.putText(img, element, (970, y_pos + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    for i, element in enumerate(elements_second):
        y_pos = i * 100 + 10
        cv2.rectangle(img, (230, y_pos), (330, y_pos + 100), (200, 200, 200), cv2.FILLED)
        cv2.putText(img, element, (250, y_pos + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Draw combination result area
    cv2.rectangle(img, (400, 10), (1220, 200), (0, 255, 0), 2)
    if selected_element1:
        cv2.putText(img, f"{selected_element1} + ", (420, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    if selected_element2:
        cv2.putText(img, selected_element2, (590, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    if result:
        cv2.putText(img, f" = {result}", (670, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

    cv2.rectangle(img, (400, 230), (1220, 630), (0, 255, 0), 2)
    cv2.putText(img, "Description area...", (420, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Process hand landmarks if detected
    if results.multi_hand_landmarks:
        for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = img.shape
            cy = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * h)

            # Check if a close gesture is made
            if is_close(hand_landmarks, img):
                current_time = time.time()
                if current_time - last_selection_time > 1:  # Only select every second
                    selected_element = get_selected_element(cy, elements_first if hand_no == 0 else elements_second)
                    if selected_element1 is None:
                        selected_element1 = selected_element
                    elif selected_element2 is None and selected_element != selected_element1:
                        selected_element2 = selected_element
                    last_selection_time = current_time  # Update last selection time
    else:
        # Reset selections if no hands are detected
        selected_element1 = None
        selected_element2 = None

    # Combine selected elements when both are chosen
    if selected_element1 and selected_element2:
        result = compounds.get((selected_element1, selected_element2), "No Match")

    # Display the "Clear" button
    cv2.putText(img, "Press 'C' to clear", (400, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Check for "Clear" button press
    if cv2.waitKey(1) & 0xFF == ord('c'):
        selected_element1 = None
        selected_element2 = None
        result = None

    # Display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (700, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    # Show the final image
    cv2.imshow("Compound Maker", img)

    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
