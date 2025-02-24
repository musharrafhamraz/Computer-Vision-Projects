from groq import Groq
import os
from dotenv import load_dotenv

class LLMEnhancer:
    def __init__(self, api_key=None):
        # Load the .env file from the current directory
        load_dotenv()
        
        # Use provided API key or fall back to .env variable
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key not provided or found in environment variable GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)

    def enhance_response(self, object_data):
        if not object_data:
            return "No object detected."
        
        label = object_data["label"]
        confidence = object_data["confidence"]
        
        # Prepare the prompt for LLaMA
        prompt = (
            f"An object was detected: '{label}' with a confidence of {confidence:.2f}. "
            "Provide a brief, natural description of what this object is and its likely everyday use."
        )
        
        # Call the Groq API with LLaMA model
        response = self.call_llm_api(prompt)
        return response

    def call_llm_api(self, prompt):
        try:
            # Create a chat completion with the LLaMA model
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",  # LLaMA 3 70B model
                max_tokens=100,  # Limit response length
                temperature=0.7,  # Adjust creativity (0.0 - 1.0)
            )
            # Extract and return the generated text
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Error calling Groq API: {str(e)}"

# Example usage
if __name__ == "__main__":
    enhancer = LLMEnhancer()
    object_data = {"label": "cup", "confidence": 0.95}
    enhanced_text = enhancer.enhance_response(object_data)
    print(enhanced_text)