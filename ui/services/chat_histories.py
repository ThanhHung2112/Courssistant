import os
import shelve

# Define the path to the history folder
HISTORY_FOLDER = "ui/histories"

# Create the history folder if it doesn't exist
if not os.path.exists(HISTORY_FOLDER):
    os.makedirs(HISTORY_FOLDER)

# Load chat history from file
def load_chat_history():
    history_file = os.path.join(HISTORY_FOLDER, "chat_history.dat")
    if os.path.exists(history_file):
        with shelve.open(history_file) as db:
            return db.get("messages", [])
    return []

# Save chat history to file
def save_chat_history(messages):
    history_file = os.path.join(HISTORY_FOLDER, "chat_history.dat")
    with shelve.open(history_file) as db:
        db["messages"] = messages