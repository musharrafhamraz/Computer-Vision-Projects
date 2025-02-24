import cv2

class Display:
    def show_frame(self, frame, text, position=(50, 50)):
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("Object Identification", frame)

    def wait_key(self):
        return cv2.waitKey(1) & 0xFF

    def close(self):
        cv2.destroyAllWindows()