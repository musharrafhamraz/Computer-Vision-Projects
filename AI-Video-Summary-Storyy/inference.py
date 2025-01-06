import os
import base64
from phi.agent import Agent
from phi.model.google import Gemini
from dotenv import load_dotenv
from llm import LLMInferenceNode

# Load environment variables
load_dotenv()

def initialize_agent():
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[],
        markdown=True,
    )

multimodal_Agent = initialize_agent()

def process_video(video_file, user_query):
    llm = LLMInferenceNode()
    if not video_file or not user_query:
        return "Error: Please provide both a video and a query."

    try:
        with open(video_file, 'rb') as f:
            video_data = f.read()

        # Generate content for video analysis
        video_prompt = """
        Analyze the uploaded video for content and context.
        Extract the main topics, events, and key elements from the video.
        Provide a detailed summary of the video content.
        """

        # Fake video analysis since `genai` isn't fully implemented
        video_analysis_text = "This is a placeholder for video analysis results."

        # Comprehensive analysis prompt for the agent
        agent_prompt = f"""
        Based on this video analysis: {video_analysis_text}
        Research and respond to the following query:
        {user_query}
        """

        agent_response = multimodal_Agent.run(agent_prompt)
        story = llm.generate_story(agent_response.content)

        return agent_response.content, story

    except Exception as e:
        return f"Error: {str(e)}"
