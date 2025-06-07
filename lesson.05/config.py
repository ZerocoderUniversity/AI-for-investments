import os
from dotenv import load_dotenv


load_dotenv()

TOKEN_TG = os.getenv("TOKEN_TG")
OPENAI_KEY = os.getenv("OPENAI_KEY")
# BASE_URL = "https://api.openai.com/v2"
BASE_URL = "https://api.proxyapi.ru/openai/v1"