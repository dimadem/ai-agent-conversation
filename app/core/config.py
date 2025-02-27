import os
from dotenv import load_dotenv

load_dotenv(".env")

OPENAI_API_KEY = os.environ.get("OPENAI_API")
YANDEX_FOLDER_ID = os.environ.get("YANDEX_FOLDER_ID")
YANDEX_API_KEY = os.environ.get("YANDEX_API_KEY")