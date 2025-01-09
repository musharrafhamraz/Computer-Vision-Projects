import cv2
import numpy as np
from ultralytics import solutions
from matplotlib import pyplot as plt


class GymTrainerGUIWithOpenCV:
    def __init__(self, backend):
        self.backend = backend

    def create_display(self, frame):
        """Creates the GUI layout overlay on the given frame."""
        # Frame dimensions
        height, width, _ = frame.shape

        # Background color
        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        canvas[:] = (32, 32, 32)  # Dark gray background

        # Title
        cv2.putText(canvas, "AI GYM Trainer", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Right Panel for Today's Plan
        cv2.rectangle(canvas, (width - 250, 30), (width - 10, height - 50), (48, 48, 48), -1)  # Dark gray panel
        cv2.rectangle(canvas, (width - 250, 30), (width - 10, height - 50), (255, 255, 255), 2)  # Border
        cv2.putText(canvas, "Today's Plan", (width - 230, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Exercises and Progress
        y_offset = 100
        for exercise, target in self.backend.plan.items():
            completed = self.backend.progress[exercise]
            text = f"{exercise}"
            progress = f"{completed}/{target}"
            cv2.putText(canvas, text, (width - 240, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(canvas, progress, (width - 130, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            y_offset += 40

        # Clear Button
        cv2.rectangle(canvas, (width - 180, height - 50), (width - 10, height - 30), (48, 48, 48), -1)  # Button
        cv2.rectangle(canvas, (width - 180, height - 50), (width - 10, height - 30), (255, 255, 255), 1)  # Border
        cv2.putText(canvas, "Clear", (width - 160, height - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Merge the GUI overlay with the frame
        blended_frame = cv2.addWeighted(frame, 0.8, canvas, 0.2, 0)
        return blended_frame

    def run(self):
        """Run the program with the updated appearance."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Cannot access the webcam.")
            return

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to grab a frame.")
                break

            # Resize frame for consistency
            frame = cv2.resize(frame, (800, 600))

            # Simulate backend progress update
            self.backend.current_exercise = self.backend.detect_exercise(self.backend.gym.monitor(frame))
            if self.backend.current_exercise:
                self.backend.progress[self.backend.current_exercise] = min(
                    self.backend.progress[self.backend.current_exercise] + 1, self.backend.plan[self.backend.current_exercise]
                )

            # Add GUI overlay
            frame_with_gui = self.create_display(frame)

            # Show the frame with GUI
            cv2.imshow("AI Gym Trainer", frame_with_gui)

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


class PersonalGymTrainer:
    def __init__(self):
        self.gym = solutions.AIGym(
            show=False,  # Disable automatic display of frames
            kpts=[6, 8, 10],  # Example keypoints for exercises
            model="yolo11s-pose.pt"  # Path to YOLO11 pose estimation model
        )
        self.plan = {}
        self.progress = {}
        self.current_exercise = None

    def create_plan(self):
        """Generate a daily plan with exercises and target reps."""
        self.plan = {
            "Pushups": 20,
            "Squats": 15,
            "Lunges": 10
        }
        self.progress = {exercise: 0 for exercise in self.plan}
        print("Workout plan created:", self.plan)

    def detect_exercise(self, results):
        """Detect the current exercise based on keypoints."""
        if results is None or not hasattr(results, 'keypoints'):
            return None

        keypoints = results.keypoints
        if len(keypoints) < 17:  # Ensure all keypoints are available
            return None

        # Extract keypoints for readability
        nose = keypoints[0]
        left_shoulder, right_shoulder = keypoints[5], keypoints[6]
        left_hip, right_hip = keypoints[11], keypoints[12]
        left_knee, right_knee = keypoints[13], keypoints[14]
        left_ankle, right_ankle = keypoints[15], keypoints[16]
        left_wrist, right_wrist = keypoints[9], keypoints[10]

        # Calculate midpoints for symmetry
        shoulder_y = (left_shoulder[1] + right_shoulder[1]) / 2
        hip_y = (left_hip[1] + right_hip[1]) / 2
        knee_y = (left_knee[1] + right_knee[1]) / 2
        ankle_y = (left_ankle[1] + right_ankle[1]) / 2
        wrist_y = (left_wrist[1] + right_wrist[1]) / 2

        # Push-Up Detection
        # Wrists are near the shoulder height during a push-up
        if wrist_y < shoulder_y + 30 and wrist_y > shoulder_y - 30:
            if hip_y > shoulder_y:  # Ensure the body is horizontal
                return "Push-Up"

        # Squat Detection
        # Hips should drop below the knee level during a squat
        if hip_y > knee_y + 30:
            if shoulder_y > hip_y:  # Ensure the torso remains upright
                return "Squat"

        # Sit-Up Detection
        # Nose or shoulders should rise above hip level during a sit-up
        if nose[1] < hip_y - 50 or shoulder_y < hip_y - 50:
            return "Sit-Up"

        return None


    def show_progress_summary(self):
        """Display the daily progress using Matplotlib."""
        exercises = list(self.plan.keys())
        completed = [self.progress[ex] for ex in exercises]
        targets = [self.plan[ex] for ex in exercises]

        x = np.arange(len(exercises))

        plt.bar(x - 0.2, completed, 0.4, label="Completed", color="green")
        plt.bar(x + 0.2, targets, 0.4, label="Target", color="blue")
        plt.xlabel("Exercises")
        plt.ylabel("Repetitions")
        plt.title("Daily Progress Summary")
        plt.xticks(x, exercises)
        plt.legend()
        plt.show()


# Run the program with the new GUI
if __name__ == "__main__":
    trainer_backend = PersonalGymTrainer()
    trainer_backend.create_plan()
    gym_gui = GymTrainerGUIWithOpenCV(trainer_backend)
    gym_gui.run()
