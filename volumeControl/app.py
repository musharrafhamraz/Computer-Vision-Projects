import cv2
from hand_tracking import HandTracker
from volume_control import VolumeControl
from utilities import calculate_distance

def main():
    # Initialize hand tracker and volume controller
    hand_tracker = HandTracker()
    volume_controller = VolumeControl()

    # Start capturing video
    capture = cv2.VideoCapture(0)
    while True:
        success, image = capture.read()
        if not success:
            break

        # Find hands
        landmarks_list = hand_tracker.find_hands(image)

        # Process landmarks if available
        if landmarks_list:
            for hand_landmarks in landmarks_list:
                positions = hand_tracker.get_landmark_positions(image, hand_landmarks)
                print(positions)  # Debug positions to verify landmark coordinates
                if 4 in positions and 8 in positions:
                    tpx, tpy = positions[4]
                    ipx, ipy = positions[8]

                    # Draw circles and line
                    cv2.circle(image, (tpx, tpy), 15, (255, 0, 255), cv2.FILLED)
                    cv2.circle(image, (ipx, ipy), 15, (255, 0, 255), cv2.FILLED)
                    cv2.line(image, (tpx, tpy), (ipx, ipy), (0, 255, 0), 3)

                    # Calculate distance and set volume
                    distance = calculate_distance((tpx, tpy), (ipx, ipy))
                    volume_controller.set_volume_by_distance(distance)
                    print(f"Distance: {distance:.2f}")

        # Display the image
        cv2.imshow("Hand Volume Control", image)

        # Exit on 'ESC'
        if cv2.waitKey(1) & 0xFF == 27:
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

