import os
from dotenv import load_dotenv


load_dotenv()

TOKEN_TG = os.getenv("TOKEN_TG")
OPENAI_KEY = os.getenv("OPENAI_KEY")