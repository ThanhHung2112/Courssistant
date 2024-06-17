import streamlit as st
import pandas as pd
from constants.global_varient import get_df_display

from services.whisper_handler.text2speech import text2speech
from components.course_grid import QnA_SQL
from components.navigate_page import navigate
from services.chat.chat_histories import save_chat_history
from services.chat.rasa_api import get_rasa_response
from services.intent_handlers.intent_classify import intent_classification, whisper_intent_classification
from services.intent_handlers.open_course import course_name_from_input, nearest_course
from constants.global_varient import set_execute_whisper, get_execute_whisper
from services.intent_handlers.course_search_intent import course_search_pipeline

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# Function to process user input
def process_user_input(chat_container, user_input):
    df = pd.read_csv("assistant/data/courssistant_main.csv")
    st.session_state.messages.append({"role": "user", "content": user_input})
    with chat_container:
        with st.chat_message("user", avatar=USER_AVATAR):
            st.write(user_input)
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            thinking = st.write("Thinking ...")
            whisper_intent = whisper_intent_classification(user_input)
            thinking = st.write(whisper_intent)
            if whisper_intent in ["whisper_on", "whisper_off"]:
                set_execute_whisper(whisper_intent == "whisper_on")
                responses = f"Whisper is {'on' if get_execute_whisper() else 'off'}"
            elif whisper_intent == 'common':
                common_intent = intent_classification(user_input)
                st.write(common_intent)
                if common_intent.lower() in ["greet", "ask_name", "ask_features", "bot_challenge"]:
                    responses = get_rasa_response(user_input)
                elif common_intent.lower() == "course_search": 
                    df, responses = course_search_pipeline(user_input)
                elif common_intent.lower() == "open_landingpage":
                    df_display = get_df_display()
                    img_src = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQN9mLqVjKSSwvlY_o4pTeOKY2oSpbQYDFcjw&s"
                    nn, result = nearest_course(df_display, course_name_from_input(user_input))
                    print(result)
                    navigate(result['Course']['CourseName'], result['Course']['University'], 
                                result['Course']['DifficultyLevel'], result['Course']['CourseRating'], result['Course']['CourseDescription'][:1000],
                                result['Course']['Specialized'],img_src)
                    st.experimental_set_query_params(page="landingpage")
                    import pages.landingpage
                    pages.landingpage 
                    st.stop()
                else:
                    df, responses = QnA_SQL(user_input)
            else:
                set_execute_whisper("whisperon" in whisper_intent)
                common_intent = intent_classification(user_input)
                st.write(common_intent)
                if common_intent.lower() in ["greet", "ask_name", "ask_features", "bot_challenge"]:
                    responses = get_rasa_response(user_input)
                elif common_intent.lower() == "course_search": 
                    df, responses = course_search_pipeline(user_input)
                elif common_intent.lower() == "open_landingpage": 
                    df_display = get_df_display()
                    img_src = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQN9mLqVjKSSwvlY_o4pTeOKY2oSpbQYDFcjw&s"
                    nn, result = nearest_course(df_display, course_name_from_input(user_input))
                    navigate(result['CourseName'], result['University'], 
                             result['DifficultyLevel'], result['CourseRating'], result['CourseDescription'],
                               result['Specialized'],img_src)
                    st.experimental_set_query_params(page="landingpage")
                    import pages.landingpage
                    pages.landingpage 
                    st.stop()
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