import gradio as gr
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
import google.generativeai as genai
from groq import Groq
import os
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google API
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

class LLMInferenceNode:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("Please set the GROQ_API_KEY environment variable.")
        self.client = Groq(api_key=self.groq_api_key)

    def generate_story(self, description):
        try:
            # Combine object names into a single sentence
            input_text = f"The following objects were detected: {description}."

            # Create the prompt
            prompt = f"Write an imaginative story involving the following objects: {description}. The story should be engaging, creative, and well-structured of around 500 words. the story should not be fictional."

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

# Initialize the phidata agent
def initialize_agent():
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )

# Create the agent instance
multimodal_Agent = initialize_agent()

# Function to process the video and query
def process_video(video_file, user_query):
    llm = LLMInferenceNode()
    if not video_file or not user_query:
        return "Error: Please provide both a video and a query."

    try:
        # Read the uploaded video file content
        with open(video_file, 'rb') as f:
            video_data = f.read()

        # Create generation config for direct Gemini API
        generation_config = {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 2048,
        }

        # Initialize the Gemini model for video processing
        model = genai.GenerativeModel('gemini-2.0-flash-exp',
                                      generation_config=generation_config)

        # Create the video analysis prompt
        video_prompt = f"""
        Analyze the uploaded video for content and context.
        Extract the main topics, events, and key elements from the video.
        Provide a detailed summary of the video content.
        """

        # Create the content for video analysis
        video_contents = {
            "parts": [
                {"text": video_prompt},
                {"inline_data": {
                    "mime_type": "video/mp4",
                    "data": base64.b64encode(video_data).decode('utf-8')
                }}
            ]
        }

        # Get video analysis
        video_analysis = model.generate_content(video_contents)

        # Create comprehensive analysis prompt for the agent
        agent_prompt = f"""
        Based on this video analysis: {video_analysis.text}
        
        Research and respond to the following query:
        {user_query}
        
        Use the search tool to gather additional context and information.
        Provide a comprehensive, well-researched response that combines 
        both the video insights and supplementary information.
        """

        # Get agent response with search capability
        agent_response = multimodal_Agent.run(agent_prompt)

        print(agent_response.content)

        story = llm.generate_story(agent_response.content)

        return agent_response.content, story

    except Exception as e:
        return f"Error: {str(e)}"


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
    description="Upload a video and specify your query to get AI-generated summaries and insights.",
    theme="compact"
)

# Launch Gradio Interface
if __name__ == "__main__":
    interface.launch()