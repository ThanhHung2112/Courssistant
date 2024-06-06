import streamlit as st
import pandas as pd
import whisper

from constants.global_varient import set_execute_whisper, get_execute_whisper
from components.course_grid import QnA_SQL, display_course_grid
from services.rasa_api import get_rasa_response
from services.intent_handlers.intent_classify import intent_classification, whisper_intent_classification
from services.whisper_handler.text2speech import text2speech
from services.whisper_handler.speech2text import get_speech_input
from services.chat.chat_histories import save_chat_history, load_chat_history
from services.chat.intent_pipeline import process_user_input

import warnings

# Suppress the warning about st.experimental_get_query_params being deprecated
warnings.filterwarnings("ignore", message=".*st.experimental_get_query_params.*", category=FutureWarning)

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

df = pd.read_csv("assistant/data/courssistant_main.csv")
# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Initialize listening state
if "is_listening" not in st.session_state:
    st.session_state.is_listening = False

# Initialize Whisper model
if "whisper_model" not in st.session_state:
    st.session_state.whisper_model = whisper.load_model("base")
def sidebar():  

    #----------------------------------------------
    # SIDEBAR
    # Sidebar with a button to delete chat history
    with st.sidebar:
        if st.button("Delete Chat History", key="rm-hisotry"):
            st.session_state.messages = []
            save_chat_history([])

    # Display chat messages in the sidebar
    with st.sidebar:
        st.header("Chat with Courssistant")
        chat_container = st.container()  # Create a container for chat messages

        # Display chat messages in reverse order (newest at the bottom)
        with chat_container:
            for i, message in enumerate(st.session_state.messages):
                avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

        # User input in the sidebar
        with st.chat_message("user"):
            user_input = st.chat_input("How can I help?", key="user_input")
            if user_input:
                df = process_user_input(chat_container, user_input)
                set_df_display(df)
            # Add microphone button
            mic_button = st.button("🎤", key="mic_button")
            if mic_button:
                if not st.session_state.is_listening:
                    st.session_state.is_listening = True
                    user_input = get_speech_input()
                    if user_input:
                        df = process_user_input(chat_container, user_input)
                        set_df_display(df)