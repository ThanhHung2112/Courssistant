import streamlit as st
import pandas as pd
import time
import pandas as pd

from constants.const import set_execute_whisper, get_execute_whisper
from components.course_grid import QnA_SQL, display_course_grid
from services.rasa_api import get_rasa_response
from services.chat_histories import save_chat_history, load_chat_history
from services.intent_handlers.intent_classify import intent_classification, whisper_intent_classification
from services.whisper_handler.speech2text import speech2text
from services.whisper_handler.text2speech import text2speech
st.title("Courssistant Page")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

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
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display the user's message
        with chat_container:
            with st.chat_message("user", avatar=USER_AVATAR):
                st.write(user_input)

        with chat_container:
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
                st.write(get_execute_whisper())
                if get_execute_whisper():
                    text2speech(full_response)
                    
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
zone = st.empty()
for userInput in userInputs:
    current = time.time()
    # df, response = QnA_SQL(userInput)
    with zone.container():
        # st.write(response)
        print(f"Finished QnA in {time.time()- current} seconds")
        display_course_grid(df[:30])
        

