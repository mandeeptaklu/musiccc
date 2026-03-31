import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    MONGO_URL = os.getenv("MONGO_URL")
    SESSION_STRING = os.getenv("SESSION_STRING")
    LOGGER_ID = int(os.getenv("LOGGER_ID", "-1003597947384"))
    # Sudo users ko list mein convert karna
    SUDO_USERS = [int(x) for x in os.getenv("SUDO_USERS", "").split()]

