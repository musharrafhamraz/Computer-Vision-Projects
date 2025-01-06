import os
from groq import Groq

class LLMInferenceNode:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("Please set the GROQ_API_KEY environment variable.")
        self.client = Groq(api_key=self.groq_api_key)

    def generate_story(self, description):
        try:
            prompt = f"Write an imaginative story involving the following objects: {description}. The story should be engaging, creative, and well-structured of around 500 words."
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
            return completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Error occurred while processing the request: {str(e)}"
