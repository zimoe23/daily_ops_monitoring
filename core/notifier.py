import json
import os
import requests
from datetime import datetime
from config.settings import CHAT_WEBHOOK_URL


class NotificationManager:
    
    @staticmethod
    def send(message):
        payload = {"text": message}

        try:
            if not CHAT_WEBHOOK_URL:
                raise ValueError("CHAT_WEBHOOK_URL environment variable is required")
            requests.post(CHAT_WEBHOOK_URL, json=payload)
        except Exception as e:
            print("Notification error:", e)

    