import streamlit as st
from services.rasa_api import get_rasa_response
from services.chat_histories import save_chat_history, load_chat_history
from services.text2sql import get_connection, QnAWithDuck, table_schema
import pandas as pd
import numpy as np
import db_config
from sqlalchemy import create_engine, text
import os
import subprocess
import time
from subprocess import Popen, PIPE
import re
from pandasai import Agent
from pandasai.llm import OpenAI




st.title("Courssistant")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"


# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

# Display chat messages in the sidebar
with st.sidebar:
    st.header("Chat with Rasa Bot")
    
    chat_container = st.container()  # Create a container for chat messages

    # Display chat messages in reverse order (newest at the bottom)
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # User input in the sidebar
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("How can I help?", key="user_input")
        submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display the user's message
        with chat_container:
            with st.chat_message("user", avatar=USER_AVATAR):
                st.markdown(user_input)
    

        responses = get_rasa_response(user_input)
        full_response = ""
        for response in responses:
            full_response += response.get("text", "")
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Display Rasa's response
        with chat_container:
            with st.chat_message("assistant", avatar=BOT_AVATAR):
                st.markdown(full_response)

        # Save chat history after each interaction
        save_chat_history(st.session_state.messages)

        
def display_course_grid(df):
    card_height = 300

    num_columns = 3
    num_rows = len(df)
    
    rows = [df.iloc[i:i + num_columns] for i in range(0, num_rows, num_columns)]

    for row in rows:
        cols = st.columns(num_columns)
        for col, (index, item) in zip(cols, row.iterrows()):
            col.markdown(f"""
            <div style="margin-bottom: 20px;">
                <div style="border: 2px solid #000; padding: 10px; border-radius: 10px; background-color: #fff; height: {card_height}px;">
                    <h2 style="color: #000;">{item['contactLastName']}</h2>
                    <p style="color: #000;"><strong>Name:</strong> {item['contactFirstName']}</p>
                    <p style="color: #000;"><strong>Country:</strong> {item['country']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

# userInput = "how many customer"
def QnA_SQL(userInput):
    engineSQL = get_connection()
    create_table_query = table_schema("customers", engineSQL)
    queryExecutable = QnAWithDuck(userInput, create_table_query)
    df = pd.read_sql_query(sql = text(queryExecutable), con = engineSQL.connect())
    print(df)
    df.to_csv("df_display.csv")
    return df

st.title("Yattaaaaaaaaa")

# df = pd.read_csv("df_display.csv")
userInputs = ["find all customer live in australia", "find all customer live in america", "find the customer with the highest credit limit"]
for userInput in userInputs:
    st.write(userInput)
    st.empty()
    df = QnA_SQL(userInput)
    display_course_grid(df)

# try:
#     agent = Agent(df_agent)
#     agent.train(docs="He is the highest")
#     response = agent.chat(question + "answer with text or dataframe")
#     print(response)
#     print(type(response))
# except:
#     print("error")