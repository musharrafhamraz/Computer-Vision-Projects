import cv2
import torch
from groq import Groq
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self):
        # Load the YOLO model
        self.model = YOLO("yolo11s.pt")

    def detect_objects(self, frame):
        # Run inference on the frame
        results = self.model(frame)

        # Extract detected object names from the results
        detected_objects = []
        for result in results:  # Iterate over the list of results
            for box in result.boxes:  # Access the detected bounding boxes
                class_index = int(box.cls)  # Get the class index
                class_name = self.model.names[class_index]  # Map index to class name
                detected_objects.append(class_name)  # Append the class name

        return detected_objects



class LLMInferenceNode:
    # def __init__(self):
    #     self.groq_api_key = ""
    #     if not self.groq_api_key:
    #         raise ValueError("Please set the GROQ_API_KEY environment variable.")
    #     self.client = Groq(api_key=self.groq_api_key)

    def generate_story(self, object_names):
        try:
            # Combine object names into a single sentence
            input_text = f"The following objects were detected: {', '.join(object_names)}."

            # Create the prompt
            prompt = f"Write an imaginative story involving the following objects: {', '.join(object_names)}. The story should be engaging, creative, and well-structured of around 500 words. the story should not be fictional."

            # Use the Groq client to generate the response
            messages = [
                {"role": "system", "content": "You are a creative storyteller."},
                {"role": "user", "content": prompt},
            ]

            completion = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=0.95,
                stream=False,
            )

            # Extract and return the story
            story = completion.choices[0].message.content.strip()
            return story
        except Exception as e:
            print(f"An error occurred: {e}")
            return f"Error occurred while processing the request: {str(e)}"

# Main program
if __name__ == "__main__":
    # Initialize object detector and LLM inference node
    detector = ObjectDetector()
    llm = LLMInferenceNode()

    # Capture video from the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        exit()

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Detect objects in the frame
        object_names = detector.detect_objects(frame)

        # Generate a story based on detected objects
        if object_names:
            story = llm.generate_story(object_names)
            print("\nGenerated Story:\n", story)
        else:
            print("No objects detected.")

        # Display the video feed
        cv2.imshow("Object Detection", frame)

        # Quit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
