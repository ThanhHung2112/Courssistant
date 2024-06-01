import streamlit as st
import pandas as pd
<<<<<<< HEAD
import numpy as np
from sqlalchemy import create_engine, text
import os
import subprocess
import time
from subprocess import Popen, PIPE
import re
from pandasai import Agent
from pandasai.llm import OpenAI
import pandas as pd
from components.course_grid import QnA_SQL, display_course_grid
from services.rasa_api import get_rasa_response
from services.chat_histories import save_chat_history, load_chat_history
from services.text2speech import Text2Speech
from services.intent_classify import intent_classification, whisper_intent_classification

from time import sleep

st.title("Courssistant Page")
=======
import time
import whisper

from constants.const import set_execute_whisper, get_execute_whisper
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

st.set_page_config(layout="wide")
>>>>>>> e14947974958d715e5f018393eacc28abbe98ac1

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

<<<<<<< HEAD
=======
df = pd.read_csv("assistant/data/coursera_main_data.csv")
>>>>>>> e14947974958d715e5f018393eacc28abbe98ac1
# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

<<<<<<< HEAD
=======
# Initialize listening state
if "is_listening" not in st.session_state:
    st.session_state.is_listening = False

# Initialize Whisper model
if "whisper_model" not in st.session_state:
    st.session_state.whisper_model = whisper.load_model("base")

>>>>>>> e14947974958d715e5f018393eacc28abbe98ac1
#----------------------------------------------
# SIDEBAR
# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

# Display chat messages in the sidebar
with st.sidebar:
    st.header("Chat with Courssistant")
<<<<<<< HEAD
    
=======

>>>>>>> e14947974958d715e5f018393eacc28abbe98ac1
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
<<<<<<< HEAD
        # submit_button = st.form_submit_button(label="Send")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display the user's message
        with chat_container:
            with st.chat_message("user", avatar=USER_AVATAR):
                st.write(user_input)

        with chat_container:
            with st.chat_message("assistant", avatar=BOT_AVATAR):
                thinking = st.write("Thinking ...")
                whisper_intent = whisper_intent_classification(user_input)

                if whisper_intent in ["whisper_on", "whisper_off"]:
                    execute_whisper = (whisper_intent == "whisper_on")
                    responses = f"Whisper is {'on' if execute_whisper else 'off'}"
                else:
                    execute_whisper = "whisperon" in whisper_intent
                    common_intent = intent_classification(user_input)
                    if common_intent in ["greet", "ask_name", "ask_features", "bot_challenge"]:
                        responses = get_rasa_response(user_input)
                    else:
                        df, responses = QnA_SQL(user_input)
                try:         
                    full_response = ""
                    for response in responses:
                        full_response += response.get("text", "")
                except:
                    full_response = responses
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                thinking = st.empty()
                st.write(full_response)

        # Save chat history after each interaction
        save_chat_history(st.session_state.messages)

#----------------------------------------------
# MAIN PAGE
st.title("Yattaaaaaaaaa")
userInputs = ["how many course with Intermediate level?"]
df = pd.read_csv("assistant/data/Coursera_2.csv")
# userInputs = ["find me 5 course with beginner level", "how many course with Intermediate level?", "find the customer with the highest credit limit"]
# zone = st.empty()
for userInput in userInputs:
    current = time.time()
    # df, response = QnA_SQL(userInput)
    with st.container():
        # st.write(response)
        print(f"Finished QnA in {time.time()- current} seconds")
        display_course_grid(df[:30])
        

=======
        if user_input:
            df = process_user_input(chat_container, user_input)

        # Add microphone button
        mic_button = st.button("🎤", key="mic_button")
        if mic_button:
            if not st.session_state.is_listening:
                st.session_state.is_listening = True
                user_input = get_speech_input()
                if user_input:
                    df = process_user_input(chat_container, user_input)

#----------------------------------------------
# MAIN PAGE
st.title("Online Courses")
zone = st.empty()
current = time.time()
with zone.container():
    print(f"Finished QnA in {time.time() - current} seconds")
    
    display_course_grid(df[:100])
>>>>>>> e14947974958d715e5f018393eacc28abbe98ac1
