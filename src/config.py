import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PAGESPEED_API_KEY = os.getenv("PAGESPEED_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")