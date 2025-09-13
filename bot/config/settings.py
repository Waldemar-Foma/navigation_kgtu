import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_NAME = os.getenv("DATABASE_NAME", "users.db")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")
