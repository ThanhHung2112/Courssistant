import streamlit as st
import pandas as pd

from services.whisper_handler.text2speech import text2speech
from components.course_grid import QnA_SQL, display_course_grid
from services.chat.chat_histories import save_chat_history, load_chat_history
from services.rasa_api import get_rasa_response
from services.intent_handlers.intent_classify import intent_classification, whisper_intent_classification
from constants.const import set_execute_whisper, get_execute_whisper

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# Function to process user input
def process_user_input(chat_container, user_input):
    df = pd.read_csv("assistant/data/coursera_main_data.csv")
    st.session_state.messages.append({"role": "user", "content": user_input})
    with chat_container:
        with st.chat_message("user", avatar=USER_AVATAR):
            st.write(user_input)
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            thinking = st.write("Thinking ...")
            whisper_intent = whisper_intent_classification(user_input)
            st.write(whisper_intent)
            if whisper_intent in ["whisper_on", "whisper_off"]:
                set_execute_whisper(whisper_intent == "whisper_on")
                responses = f"Whisper is {'on' if get_execute_whisper() else 'off'}"
            elif whisper_intent == 'common':
                common_intent = intent_classification(user_input)
                st.write(common_intent)
                if common_intent.lower() in ["greet", "ask_name", "ask_features", "bot_challenge"]:
                    responses = get_rasa_response(user_input)
                else:
                    df, responses = QnA_SQL(user_input)
            else:
                set_execute_whisper("whisperon" in whisper_intent)
                common_intent = intent_classification(user_input)
                st.write(common_intent)
                if common_intent.lower() in ["greet", "ask_name", "ask_features", "bot_challenge"]:
                    responses = get_rasa_response(user_input)
                else:
                    df, responses = QnA_SQL(user_input)
            try:
                full_response = ""
                for response in responses:
                    full_response += response.get("text", "")
            except:
                full_response = responses
            # text 2 speech
            st.write("whisper_status: ", get_execute_whisper())
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            thinking = st.empty()
            st.write(full_response)
            if get_execute_whisper():
                text2speech(full_response)

    save_chat_history(st.session_state.messages)

    return df