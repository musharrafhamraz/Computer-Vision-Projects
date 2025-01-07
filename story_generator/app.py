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
    def __init__(self):
        self.groq_api_key = "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"
        if not self.groq_api_key:
            raise ValueError("Please set the GROQ_API_KEY environment variable.")
        self.client = Groq(api_key=self.groq_api_key)

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

# import cv2
# import torch
# from groq import Groq
# from ultralytics import YOLO
# import gradio as gr
# import numpy as np

# class ObjectDetector:
#     def __init__(self):
#         # Load the YOLO model
#         self.model = YOLO("yolo11s.pt")

#     def detect_objects(self, frame):
#         # Run inference on the frame
#         results = self.model(frame)

#         # Extract detected object names from the results
#         detected_objects = []
#         for result in results:  # Iterate over the list of results
#             for box in result.boxes:  # Access the detected bounding boxes
#                 class_index = int(box.cls)  # Get the class index
#                 class_name = self.model.names[class_index]  # Map index to class name
#                 detected_objects.append(class_name)  # Append the class name

#         return detected_objects


# class LLMInferenceNode:
#     def __init__(self):
#         self.groq_api_key = "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"
#         if not self.groq_api_key:
#             raise ValueError("Please set the GROQ_API_KEY environment variable.")
#         self.client = Groq(api_key=self.groq_api_key)

#     def generate_story(self, object_names):
#         try:
#             # Combine object names into a single sentence
#             input_text = f"The following objects were detected: {', '.join(object_names)}."

#             # Create the prompt
#             prompt = f"Write an imaginative story involving the following objects: {', '.join(object_names)}. The story should be engaging, creative, and well-structured of around 500 words."

#             # Use the Groq client to generate the response
#             messages = [
#                 {"role": "system", "content": "You are a creative storyteller."},
#                 {"role": "user", "content": prompt},
#             ]

#             completion = self.client.chat.completions.create(
#                 model="mixtral-8x7b-32768",
#                 messages=messages,
#                 temperature=0.7,
#                 max_tokens=1024,
#                 top_p=0.95,
#                 stream=False,
#             )

#             # Extract and return the story
#             story = completion.choices[0].message.content.strip()
#             return story
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return f"Error occurred while processing the request: {str(e)}"


# # Initialize ObjectDetector and LLMInferenceNode
# detector = ObjectDetector()
# llm = LLMInferenceNode()


# def process_frame_and_generate_story(video_frame):
#     if video_frame is None or not isinstance(video_frame, (np.ndarray, list)):
#         return None, "No valid frame received from the webcam."

#     # Convert video frame to BGR format for object detection
#     frame = cv2.cvtColor(video_frame, cv2.COLOR_RGB2BGR)

#     # Detect objects in the frame
#     object_names = detector.detect_objects(frame)

#     # Generate a story based on detected objects
#     if object_names:
#         story = llm.generate_story(object_names)
#     else:
#         story = "No objects detected in the frame."
    
#     # Convert back to RGB for display in Gradio
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     return frame_rgb, story


# # Gradio UI setup
# def create_ui():
#     with gr.Blocks() as demo:
#         gr.Markdown("<h1 style='text-align: center;'>Object Detection Story Generator</h1>")
        
#         # Live video feed
#         webcam_feed = gr.Video( sources=["webcam"], label="Live Camera Feed")
        
#         # Outputs for the processed frame and the generated story
#         processed_frame = gr.Image(label="Processed Frame")
#         story_output = gr.Textbox(label="Generated Story", lines=20, interactive=False)
        
#         # Generate story button
#         generate_button = gr.Button("Generate Story")
        
#         # Click event for the Generate button
#         generate_button.click(
#             fn=process_frame_and_generate_story,
#             inputs=[webcam_feed],
#             outputs=[processed_frame, story_output],
#         )
    
#     return demo


# # Launch the Gradio app
# if __name__ == "__main__":
#     create_ui().launch()


