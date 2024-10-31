# import cv2
# import mediapipe as mp
# import numpy as np
# import random
# import time
# import math

# class handDetector():
#     def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
#         self.mode = mode
#         self.maxHands = maxHands
#         self.detectionCon = detectionCon
#         self.trackCon = trackCon

#         self.mpHands = mp.solutions.hands
#         self.hands = self.mpHands.Hands(static_image_mode=self.mode,
#                                         max_num_hands=self.maxHands,
#                                         min_detection_confidence=self.detectionCon,
#                                         min_tracking_confidence=self.trackCon)
#         self.mpDraw = mp.solutions.drawing_utils

#     def findHands(self, img, draw=True):
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         self.results = self.hands.process(imgRGB)
#         if self.results.multi_hand_landmarks:
#             for handLms in self.results.multi_hand_landmarks:
#                 if draw:
#                     self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
#         return img

#     def findPosition(self, img, handNo=0):
#         lmList = []
#         if self.results.multi_hand_landmarks:
#             myHand = self.results.multi_hand_landmarks[handNo]
#             for id, lm in enumerate(myHand.landmark):
#                 h, w, c = img.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#                 lmList.append((id, cx, cy))
#         return lmList

# def draw_grid(img):
#     """Draws a 3x3 Tic-Tac-Toe grid on the image."""
#     h, w, _ = img.shape
#     step_x = w // 3
#     step_y = h // 3
#     for i in range(1, 3):
#         # Draw vertical lines
#         cv2.line(img, (i * step_x, 0), (i * step_x, h), (255, 255, 255), 2)
#         # Draw horizontal lines
#         cv2.line(img, (0, i * step_y), (w, i * step_y), (255, 255, 255), 2)
#     return step_x, step_y

# def get_cell(x, y, step_x, step_y):
#     """Returns the grid cell based on x, y coordinates."""
#     row, col = y // step_y, x // step_x
#     return int(row), int(col)

# def draw_symbol(img, symbol, cell, step_x, step_y):
#     """Draws the 'X' or 'O' symbol in the specified cell."""
#     x_center = cell[1] * step_x + step_x // 2
#     y_center = cell[0] * step_y + step_y // 2
#     if symbol == 'X':
#         cv2.line(img, (x_center - 20, y_center - 20), (x_center + 20, y_center + 20), (0, 0, 255), 3)
#         cv2.line(img, (x_center + 20, y_center - 20), (x_center - 20, y_center + 20), (0, 0, 255), 3)
#     elif symbol == 'O':
#         cv2.circle(img, (x_center, y_center), 20, (255, 0, 0), 3)

# def check_win(board, player):
#     """Checks if the given player has won."""
#     win_conditions = [
#         [board[0][0], board[0][1], board[0][2]],
#         [board[1][0], board[1][1], board[1][2]],
#         [board[2][0], board[2][1], board[2][2]],
#         [board[0][0], board[1][0], board[2][0]],
#         [board[0][1], board[1][1], board[2][1]],
#         [board[0][2], board[1][2], board[2][2]],
#         [board[0][0], board[1][1], board[2][2]],
#         [board[0][2], board[1][1], board[2][0]],
#     ]
#     return [player, player, player] in win_conditions

# def computer_move(board):
#     """Randomly chooses an empty cell for the computer's move."""
#     empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == '']
#     return random.choice(empty_cells) if empty_cells else None

# def finger_distance(lmList, index_id, middle_id):
#     """Calculates the distance between the index and middle fingertips."""
#     x1, y1 = lmList[index_id][1], lmList[index_id][2]
#     x2, y2 = lmList[middle_id][1], lmList[middle_id][2]
#     return math.hypot(x2 - x1, y2 - y1)

# def reset_game():
#     """Resets the game board."""
#     return [["" for _ in range(3)] for _ in range(3)], False, True

# def main():
#     cap = cv2.VideoCapture(0)
#     detector = handDetector()
#     board, game_over, player_turn = reset_game()
#     step_x, step_y = 0, 0
#     last_click_time = 0
#     click_delay = 1  # seconds

#     while True:
#         success, img = cap.read()
#         img = detector.findHands(img)
#         lmList = detector.findPosition(img)

#         if step_x == 0 or step_y == 0:
#             step_x, step_y = draw_grid(img)

#         # Display labels
#         cv2.putText(img, "Computer: O", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#         cv2.putText(img, "Player: X", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#         if game_over:
#             # Display the end-game message
#             message = "You Win!" if not player_turn else "You Lose!"
#             cv2.putText(img, message, (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0) if not player_turn else (0, 0, 255), 3)

#             # Display the restart button
#             button_x1, button_y1 = 150, 300
#             button_x2, button_y2 = 350, 350
#             cv2.rectangle(img, (button_x1, button_y1), (button_x2, button_y2), (200, 200, 200), -1)
#             cv2.putText(img, "Restart", (button_x1 + 30, button_y1 + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

#             # Check for click on the restart button
#             if lmList:
#                 if button_x1 < lmList[8][1] < button_x2 and button_y1 < lmList[8][2] < button_y2:
#                     board, game_over, player_turn = reset_game()

#         else:
#             draw_grid(img)

#             if player_turn and lmList:
#                 if finger_distance(lmList, 8, 12) < 20:
#                     fingertip = lmList[8][1:3]
#                     cell = get_cell(fingertip[0], fingertip[1], step_x, step_y)

#                     if board[cell[0]][cell[1]] == "" and time.time() - last_click_time > click_delay:
#                         board[cell[0]][cell[1]] = 'X'
#                         last_click_time = time.time()
#                         draw_symbol(img, 'X', cell, step_x, step_y)
#                         if check_win(board, 'X'):
#                             game_over = True
#                         player_turn = False

#             elif not player_turn:
#                 move = computer_move(board)
#                 if move:
#                     board[move[0]][move[1]] = 'O'
#                     draw_symbol(img, 'O', move, step_x, step_y)
#                     if check_win(board, 'O'):
#                         game_over = True
#                 player_turn = True

#             for r in range(3):
#                 for c in range(3):
#                     if board[r][c] != "":
#                         draw_symbol(img, board[r][c], (r, c), step_x, step_y)

#         cv2.imshow("Tic-Tac-Toe", img)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()
import cv2
import mediapipe as mp
import numpy as np
import random
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))
        return lmList

def draw_grid(img):
    """Draws a 3x3 Tic-Tac-Toe grid on the image."""
    h, w, _ = img.shape
    step_x = w // 3
    step_y = h // 3
    for i in range(1, 3):
        # Draw vertical lines
        cv2.line(img, (i * step_x, 0), (i * step_x, h), (255, 255, 255), 2)
        # Draw horizontal lines
        cv2.line(img, (0, i * step_y), (w, i * step_y), (255, 255, 255), 2)
    return step_x, step_y

def get_cell(x, y, step_x, step_y):
    """Returns the grid cell based on x, y coordinates."""
    row, col = y // step_y, x // step_x
    return int(row), int(col)

def draw_symbol(img, symbol, cell, step_x, step_y):
    """Draws the 'X' or 'O' symbol in the specified cell."""
    x_center = cell[1] * step_x + step_x // 2
    y_center = cell[0] * step_y + step_y // 2
    if symbol == 'X':
        cv2.line(img, (x_center - 20, y_center - 20), (x_center + 20, y_center + 20), (0, 0, 255), 3)
        cv2.line(img, (x_center + 20, y_center - 20), (x_center - 20, y_center + 20), (0, 0, 255), 3)
    elif symbol == 'O':
        cv2.circle(img, (x_center, y_center), 20, (255, 0, 0), 3)

def check_win(board, player):
    """Checks if the given player has won."""
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    return [player, player, player] in win_conditions

def check_tie(board):
    """Checks if the game is a tie."""
    return all(cell != "" for row in board for cell in row)

def computer_move(board):
    """Randomly chooses an empty cell for the computer's move."""
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == '']
    return random.choice(empty_cells) if empty_cells else None

def finger_distance(lmList, index_id, middle_id):
    """Calculates the distance between the index and middle fingertips."""
    x1, y1 = lmList[index_id][1], lmList[index_id][2]
    x2, y2 = lmList[middle_id][1], lmList[middle_id][2]
    return math.hypot(x2 - x1, y2 - y1)

def reset_game():
    """Resets the game board."""
    return [["" for _ in range(3)] for _ in range(3)], False, True, False

def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    board, game_over, player_turn, is_tie = reset_game()
    step_x, step_y = 0, 0
    last_click_time = 0
    click_delay = 1  # seconds

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if step_x == 0 or step_y == 0:
            step_x, step_y = draw_grid(img)

        # Display labels
        cv2.putText(img, "Computer: O", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, "Player: X", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if game_over:
            # Display end-game message based on win or tie
            if is_tie:
                message = "Game Tied!"
            else:
                message = "You Win!" if not player_turn else "You Lose!"
            cv2.putText(img, message, (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0) if not player_turn else (0, 0, 255), 3)

            # Display the restart button
            button_x1, button_y1 = 150, 300
            button_x2, button_y2 = 350, 350
            cv2.rectangle(img, (button_x1, button_y1), (button_x2, button_y2), (200, 200, 200), -1)
            cv2.putText(img, "Restart", (button_x1 + 30, button_y1 + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            # Check for click on the restart button
            if lmList:
                if button_x1 < lmList[8][1] < button_x2 and button_y1 < lmList[8][2] < button_y2:
                    board, game_over, player_turn, is_tie = reset_game()

        else:
            draw_grid(img)

            if player_turn and lmList:
                if finger_distance(lmList, 8, 12) < 20:
                    fingertip = lmList[8][1:3]
                    cell = get_cell(fingertip[0], fingertip[1], step_x, step_y)

                    if board[cell[0]][cell[1]] == "" and time.time() - last_click_time > click_delay:
                        board[cell[0]][cell[1]] = 'X'
                        last_click_time = time.time()
                        draw_symbol(img, 'X', cell, step_x, step_y)
                        if check_win(board, 'X'):
                            game_over = True
                        elif check_tie(board):
                            game_over = True
                            is_tie = True
                        player_turn = False

            elif not player_turn:
                move = computer_move(board)
                if move:
                    board[move[0]][move[1]] = 'O'
                    draw_symbol(img, 'O', move, step_x, step_y)
                    if check_win(board, 'O'):
                        game_over = True
                    elif check_tie(board):
                        game_over = True
                        is_tie = True
                player_turn = True

            for r in range(3):
                for c in range(3):
                    if board[r][c] != "":
                        draw_symbol(img, board[r][c], (r, c), step_x, step_y)

        cv2.imshow("Tic-Tac-Toe", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
