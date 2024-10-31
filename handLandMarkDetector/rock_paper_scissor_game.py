import cv2
import mediapipe as mp
import time
import random


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

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        return lmList

    def detectGesture(self, lmList):
        """Detects rock, paper, or scissors based on landmarks."""
        if not lmList:
            return None

        # Rock: All fingers are closed
        if lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2]:
            return "rock"
        # Scissors: Only index and middle fingers are open
        elif lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] > lmList[14][2]:
            return "scissors"
        # Paper: All fingers are open
        elif lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2]:
            return "paper"
        return None


def playRPS(playerGesture, computerChoice):
    """Returns the result of the game based on player and computer choices."""
    if playerGesture == computerChoice:
        return "Tie"
    elif (playerGesture == "rock" and computerChoice == "scissors") or \
         (playerGesture == "scissors" and computerChoice == "paper") or \
         (playerGesture == "paper" and computerChoice == "rock"):
        return "Player Wins"
    else:
        return "Computer Wins"


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    scores = {"Player": 0, "Computer": 0, "Ties": 0}
    gameStarted = False
    startTime = 0

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        # Detect player gesture
        playerGesture = detector.detectGesture(lmList)

        # Show player gesture on the screen
        if playerGesture:
            cv2.putText(img, f"Player: {playerGesture}", (10, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        # Start a new game round after a delay
        if not gameStarted:
            startTime = time.time()
            gameStarted = True
            computerChoice = random.choice(["rock", "paper", "scissors"])

        # After 3 seconds, check the result
        if gameStarted and time.time() - startTime > 3:
            if playerGesture:
                result = playRPS(playerGesture, computerChoice)
                if result == "Player Wins":
                    scores["Player"] += 1
                elif result == "Computer Wins":
                    scores["Computer"] += 1
                else:
                    scores["Ties"] += 1

                # Show computer choice and result
                cv2.putText(img, f"Computer: {computerChoice}", (10, 200), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
                cv2.putText(img, result, (10, 250), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

                # Reset game state
                gameStarted = False

        # Display the FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        # Display the score
        cv2.putText(img, f"Player: {scores['Player']}  Computer: {scores['Computer']}  Ties: {scores['Ties']}",
                    (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

        cv2.imshow('Rock Paper Scissors Game', img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
