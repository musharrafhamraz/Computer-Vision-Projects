import gradio as gr
from inference import process_video

# Define Gradio UI
video_input = gr.Video(sources=["upload"], label="Upload Video")
text_input = gr.Textbox(label="Enter Query", placeholder="Specify your query...")
output_text = gr.Textbox(label="AI Summary")
story_text = gr.Textbox(label="Generated Story")

interface = gr.Interface(
    fn=process_video,
    inputs=[video_input, text_input],
    outputs=[output_text, story_text],
    title="Video Summarizer - Story Generator",
    description="Upload a video and specify your query to get AI-generated summaries and story.",
    theme="compact"
)

# Launch Gradio Interface
if __name__ == "__main__":
    interface.launch()
