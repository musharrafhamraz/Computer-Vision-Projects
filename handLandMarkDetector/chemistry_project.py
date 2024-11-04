# import cv2
# import mediapipe as mp
# import time

# # Combined element list and expanded compounds
# elements_first = ["O", "Se", "Ca", "He", "S", "N", "Mg", "C", "Cl"]
# elements_second = ["H", "Na", "Bi"]
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
# descriptions = {
#     ("H₂O"): """Water (H₂O) is essential for all known forms 
# of life. It is a colorless, tasteless, and odorless 
# liquid at room temperature. Water molecules are 
# polar, enabling them to dissolve many substances.""",

#     ("NaCl"): """Sodium chloride (NaCl), commonly known as 
# table salt, is used widely in cooking and food 
# preservation. It is an ionic compound, where 
# sodium and chlorine are held by strong bonds.""",

#     ("MgO"): """Magnesium oxide (MgO) is a white powder 
# commonly used in antacids and as a laxative. It 
# forms when magnesium reacts with oxygen, 
# creating a highly stable ionic compound.""",

#     ("CO₂"): """Carbon dioxide (CO₂) is a colorless, 
# odorless gas that is a byproduct of respiration 
# and combustion. Plants use it in photosynthesis, 
# converting it to oxygen and glucose.""",

#     ("HCl"): """Hydrochloric acid (HCl) is a strong acid 
# used in various industrial processes, including 
# metal refining and cleaning. It also occurs in 
# small amounts in the stomach.""",

#     ("CaO"): """Calcium oxide (CaO), or quicklime, is a 
# white, caustic substance used in cement, 
# construction, and waste treatment. It forms 
# when calcium reacts with oxygen.""",

#     ("Na₂O"): """Sodium oxide (Na₂O) is a basic oxide that 
# reacts with water to form sodium hydroxide. It 
# is used in ceramics and glass manufacturing 
# and must be handled with care.""",

#     ("SO₂"): """Sulfur dioxide (SO₂) is a gas with a 
# pungent smell, often formed during the 
# combustion of fossil fuels. It is used in 
# preservation and the production of sulfuric acid.""",

#     ("NO₂"): """Nitrogen dioxide (NO₂) is a reddish-brown 
# gas with a sharp odor. It is a major pollutant, 
# contributing to smog and acid rain, and is 
# produced from vehicle emissions.""",
# }


# # Initialize Mediapipe for hand tracking
# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
# hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# # Variables to store selected elements and result
# selected_element1 = None
# selected_element2 = None
# result = None
# last_selection_time = 0  # To prevent rapid selections

# # Coordinates for the starting position of the text
# x, y = 220, 300
# line_height = 30  # Adjust this value to control the spacing between lines

# # Function to detect if fingers are close
# def is_close(hand_landmarks, img, threshold=30):
#     h, w, _ = img.shape
#     index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
#     middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

#     ix, iy = int(index_finger.x * w), int(index_finger.y * h)
#     mx, my = int(middle_finger.x * w), int(middle_finger.y * h)
#     distance = ((ix - mx) ** 2 + (iy - my) ** 2) ** 0.5
#     return distance < threshold

# # Function to check if a point is within a rectangle
# def is_within_box(x, y, box_x, box_y, box_width, box_height):
#     return box_x <= x <= box_x + box_width and box_y <= y <= box_y + box_height

# # Function to get selected element based on fingertip position
# def get_selected_element(x, y):
#     # Check if the fingertip is over an element in elements_first (top row)
#     for i, element in enumerate(elements_first):
#         box_x = i * 120 + 50
#         box_y = 10
#         if is_within_box(x, y, box_x, box_y, 100, 80):  # Width=100, Height=80 for each element box
#             return element

#     # Check if the fingertip is over an element in elements_second (left column)
#     for i, element in enumerate(elements_second):
#         box_x = 50
#         box_y = i * 100 + 150
#         if is_within_box(x, y, box_x, box_y, 100, 80):
#             return element

#     return None

# # # Initialize camera and set resolution
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)

# pTime = 0  # To calculate FPS

# # Main loop (continuing with the rest of your code)
# while True:
#     success, img = cap.read()
#     if not success:
#         break

#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     # Draw elements_first in a row across the top of the screen
#     for i, element in enumerate(elements_first):
#         x_pos = i * 120 + 50
#         y_pos = 10
#         cv2.rectangle(img, (x_pos, y_pos), (x_pos + 100, y_pos + 80), (200, 200, 200), cv2.FILLED)
#         cv2.putText(img, element, (x_pos + 20, y_pos + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

#     # Draw elements_second in a column along the left side of the screen
#     for i, element in enumerate(elements_second):
#         x_pos = 50
#         y_pos = i * 100 + 120
#         cv2.rectangle(img, (x_pos, y_pos), (x_pos + 100, y_pos + 80), (200, 200, 200), cv2.FILLED)
#         cv2.putText(img, element, (x_pos + 20, y_pos + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    

#     # Draw combination result area
#     cv2.rectangle(img, (200, 100), (1220, 200), (0, 255, 0), 2)
#     if selected_element1:
#         cv2.putText(img, f"{selected_element1} + ", (220, 170), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
#     if selected_element2:
#         cv2.putText(img, selected_element2, (390, 170), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
#     if result:
#         cv2.putText(img, f" = {result}", (470, 170), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

#     cv2.rectangle(img, (200, 230), (1220, 630), (0, 255, 0), 2)
#     # Loop through each line and display it
#     for i, line in enumerate(description.splitlines()):
#         cv2.putText(img, line, (x, y + i * line_height), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#     # Process hand landmarks if detected
#     if results.multi_hand_landmarks:
#         for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
#             mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#             # Get coordinates of the middle fingertip
#             h, w, _ = img.shape
#             tip_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * w)
#             tip_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * h)

#             # Check if a close gesture is made
#             if is_close(hand_landmarks, img):
#                 current_time = time.time()
#                 if current_time - last_selection_time > 1:  # Only select every second
#                     selected_element = get_selected_element(tip_x, tip_y)
#                     if selected_element1 is None:
#                         selected_element1 = selected_element
#                         print(f'First Element: {selected_element1}')
#                     elif selected_element2 is None and selected_element != selected_element1:
#                         selected_element2 = selected_element
#                         print(f'Second Element: {selected_element2}')
#                     last_selection_time = current_time  # Update last selection time
#     # else:
#     #     # Reset selections if no hands are detected
#     #     selected_element1 = None
#     #     selected_element2 = None

#     # Combine selected elements when both are chosen
#     if selected_element1 and selected_element2:
#         result = compounds.get((selected_element1, selected_element2), "No Match")

#     # Display the "Clear" button below the equation box
#     cv2.putText(img, "Press 'C' to clear", (200, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, f'FPS: {int(fps)}', (1000, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

#     # Check for "Clear" button press
#     if cv2.waitKey(1) & 0xFF == ord('c'):
#         selected_element1 = None
#         selected_element2 = None
#         result = None

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
elements_first = ["O", "Se", "Ca", "He", "S", "N", "Mg", "C", "Cl"]
elements_second = ["H", "Na", "Bi"]
compounds = {
    ("H", "O"): "H2O",
    ("Na", "Cl"): "NaCl",
    ("Mg", "O"): "MgO",
    ("C", "O"): "CO2",
    ("H", "Cl"): "HCl",
    ("Ca", "O"): "CaO",
    ("Na", "O"): "Na2O",
    ("S", "O"): "SO2",
    ("N", "O"): "NO2",
}
descriptions = {
    "H2O": """Water (H2O) is essential for all known forms 
of life. It is a colorless, tasteless, and odorless 
liquid at room temperature. Water molecules are 
polar, enabling them to dissolve many substances.""",

    "NaCl": """Sodium chloride (NaCl), commonly known as 
table salt, is used widely in cooking and food 
preservation. It is an ionic compound, where 
sodium and chlorine are held by strong bonds.""",

    "MgO": """Magnesium oxide (MgO) is a white powder 
commonly used in antacids and as a laxative. It 
forms when magnesium reacts with oxygen, 
creating a highly stable ionic compound.""",

    "CO2": """Carbon dioxide (CO2) is a colorless, 
odorless gas that is a byproduct of respiration 
and combustion. Plants use it in photosynthesis, 
converting it to oxygen and glucose.""",

    "HCl": """Hydrochloric acid (HCl) is a strong acid 
used in various industrial processes, including 
metal refining and cleaning. It also occurs in 
small amounts in the stomach.""",

    "CaO": """Calcium oxide (CaO), or quicklime, is a 
white, caustic substance used in cement, 
construction, and waste treatment. It forms 
when calcium reacts with oxygen.""",

    "Na2O": """Sodium oxide (Na2O) is a basic oxide that 
reacts with water to form sodium hydroxide. It 
is used in ceramics and glass manufacturing 
and must be handled with care.""",

    "SO2": """Sulfur dioxide (SO₂) is a gas with a 
pungent smell, often formed during the 
combustion of fossil fuels. It is used in 
preservation and the production of sulfuric acid.""",

    "NO2": """Nitrogen dioxide (NO2) is a reddish-brown 
gas with a sharp odor. It is a major pollutant, 
contributing to smog and acid rain, and is 
produced from vehicle emissions.""",
}

# Initialize Mediapipe for hand tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Variables to store selected elements, result, and description
selected_element1 = None
selected_element2 = None
result = None
description = ""
last_selection_time = 0  # To prevent rapid selections

# Coordinates for the starting position of the text
x, y = 220, 300
line_height = 30  # Adjust this value to control the spacing between lines

# Function to detect if fingers are close
def is_close(hand_landmarks, img, threshold=30):
    h, w, _ = img.shape
    index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

    ix, iy = int(index_finger.x * w), int(index_finger.y * h)
    mx, my = int(middle_finger.x * w), int(middle_finger.y * h)
    distance = ((ix - mx) ** 2 + (iy - my) ** 2) ** 0.5
    return distance < threshold

# Function to check if a point is within a rectangle
def is_within_box(x, y, box_x, box_y, box_width, box_height):
    return box_x <= x <= box_x + box_width and box_y <= y <= box_y + box_height

# Function to get selected element based on fingertip position
def get_selected_element(x, y):
    # Check if the fingertip is over an element in elements_first (top row)
    for i, element in enumerate(elements_first):
        box_x = i * 120 + 50
        box_y = 10
        if is_within_box(x, y, box_x, box_y, 100, 80):  # Width=100, Height=80 for each element box
            return element

    # Check if the fingertip is over an element in elements_second (left column)
    for i, element in enumerate(elements_second):
        box_x = 50
        box_y = i * 100 + 150
        if is_within_box(x, y, box_x, box_y, 100, 80):
            return element

    return None

# Initialize camera and set resolution
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

pTime = 0  # To calculate FPS

# Main loop
while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Draw elements_first in a row across the top of the screen
    for i, element in enumerate(elements_first):
        x_pos = i * 120 + 50
        y_pos = 10
        cv2.rectangle(img, (x_pos, y_pos), (x_pos + 100, y_pos + 80), (200, 200, 200), cv2.FILLED)
        cv2.putText(img, element, (x_pos + 20, y_pos + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Draw elements_second in a column along the left side of the screen
    for i, element in enumerate(elements_second):
        x_pos = 50
        y_pos = i * 100 + 120
        cv2.rectangle(img, (x_pos, y_pos), (x_pos + 100, y_pos + 80), (200, 200, 200), cv2.FILLED)
        cv2.putText(img, element, (x_pos + 20, y_pos + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Draw combination result area
    cv2.rectangle(img, (200, 100), (1220, 200), (0, 255, 0), 2)
    if selected_element1:
        cv2.putText(img, f"{selected_element1} + ", (220, 170), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    if selected_element2:
        cv2.putText(img, selected_element2, (390, 170), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    if result:
        cv2.putText(img, f" = {result}", (470, 170), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

    cv2.rectangle(img, (200, 230), (1220, 630), (0, 255, 0), 2)
    # Loop through each line of the description and display it
    for i, line in enumerate(description.splitlines()):
        cv2.putText(img, line, (x, y + i * line_height), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Process hand landmarks if detected
    if results.multi_hand_landmarks:
        for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates of the middle fingertip
            h, w, _ = img.shape
            tip_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * w)
            tip_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * h)

            # Check if a close gesture is made
            if is_close(hand_landmarks, img):
                current_time = time.time()
                if current_time - last_selection_time > 1:  # Only select every second
                    selected_element = get_selected_element(tip_x, tip_y)
                    if selected_element1 and selected_element2:
                        selected_element1, selected_element2 = None, None
                        result, description = "", ""
                    if selected_element:
                        if not selected_element1:
                            selected_element1 = selected_element
                        elif not selected_element2:
                            selected_element2 = selected_element
                            result = compounds.get((selected_element1, selected_element2), "No Match")
                            description = descriptions.get(result, "No information available for this compound.")
                    last_selection_time = current_time

    # Calculate FPS and display on the screen

    cv2.putText(img, "Press 'C' to clear", (200, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (1000, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)


    # Check for "Clear" button press
    if cv2.waitKey(1) & 0xFF == ord('c'):
        selected_element1 = None
        selected_element2 = None
        result = None
        description = ''' '''

    # Show the frame
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
