import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Rasa server URL from environment variables
RASA_SERVER_URL = os.getenv("RASA_SERVER_URL", "http://localhost:5005/webhooks/rest/webhook")

# Get response from Rasa
def get_rasa_response(message):
    payload = {
        "sender": "user",
        "message": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(RASA_SERVER_URL, json=payload, headers=headers)
    return response.json()
