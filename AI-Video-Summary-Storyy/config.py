import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

if not GROQ_API_KEY:
    raise ValueError("Please set the GROQ_API_KEY environment variable.")
