from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Google Sheets
# Get the JSON credentials filename from env
creds_file = os.getenv("GOOGLE_CREDENTIALS_FILE")
if not creds_file:
    raise ValueError("GOOGLE_CREDENTIALS_FILE environment variable is required")

# Build the full path
JSON_CREDS_PATH: str = os.path.join(BASE_DIR, "credentials", creds_file)
GOOGLE_SHEET_ID: str = os.getenv("GOOGLE_SHEET_ID") or ""
TARGET_TAB_NAME: str = os.getenv("TARGET_TAB_NAME") or ""

# DataWorks
AK_ID: str = os.getenv("AK_ID") or ""
AK_SECRET: str = os.getenv("AK_SECRET") or ""
REGION: str = os.getenv("REGION") or ""
# SLA
DAY_BEHIND: int = int(os.getenv("DAY_BEHIND") or 1)

# Notification
CHAT_WEBHOOK_URL = os.getenv("CHAT_WEBHOOK")

# Files
LOG_FILE = os.path.join(BASE_DIR, "logs", "logs.txt")