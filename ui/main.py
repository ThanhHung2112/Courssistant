import streamlit as st
from services.rasa_api import get_rasa_response
from services.chat_histories import save_chat_history, load_chat_history
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
    st.title("Yattaaaaaaaaa")

    card_height = 300

    num_columns = 3
    num_rows = len(df)
    
    rows = [df.iloc[i:i + num_columns] for i in range(0, num_rows, num_columns)]

    for row in rows:
        cols = st.columns(num_columns)
        for col, (index, item) in zip(cols, row.iterrows()):
            col.markdown(f"""
            <div style="margin-bottom: 20px;">
                <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 10px; height: {card_height}px;">
                    <h2 style="color: #4CAF50;">{item['contactLastName']}</h2>
                    <p><strong>Name:</strong> {item['contactFirstName']}</p>
                    <p><strong>Country:</strong> {item['country']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

question = st.text_input("QnA with Duck", "")

def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            db_config.db_user, db_config.db_password, db_config.db_host, db_config.db_port, db_config.db_name
        )
    )

engine = get_connection()
table_name = "customers"
with engine.connect() as connection:
    query = text("DESCRIBE {}".format(table_name))
    result = connection.execute(query)
    table_structure = result.fetchall()

create_table_query = "CREATE TABLE {} (".format(table_name)


for column in table_structure:
    column_name = column[0]
    column_type = column[1]
    create_table_query += "{} {}, ".format(column_name, column_type)

create_table_query = create_table_query[:-2] + ")"



os.environ["PANDASAI_API_KEY"] = "$2a$10$lwbP.akrhl.4fXNcDF/oQu5jcUArQwhXCXHNmcoTIYDQAsWEGeHn6"


llm = OpenAI(
    api_token="sk-proj-R3zUuZVlUot3lkumt10LT3BlbkFJkYOT041i5sCtoqxHswr4",
)

def QnAWithDuck(question, schema):
    current = time.time()
    p = subprocess.Popen("ollama run duckdb-nsql",
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True)
    promt_input = schema + question + "(response with all field from database)"
    out, _ = p.communicate(input=promt_input.encode())
    final_query = out.decode('utf-8').strip()    
    final_query = final_query.split('\n', 1)[0].strip()
    print(f'get query {final_query} in {time.time() -  current}')
    return final_query

executable_query = QnAWithDuck(question, create_table_query)
print(executable_query)

df_agent = pd.read_sql_query(sql = text(executable_query), con = engine.connect())
print(df_agent)
df_agent.to_csv("df_display.csv")


df = pd.read_csv("df_display.csv")
st.dataframe(df.iloc[:, :3])
display_course_grid(df)

# try:
#     agent = Agent(df_agent)
#     agent.train(docs="He is the highest")
#     response = agent.chat(question + "answer with text or dataframe")
#     print(response)
#     print(type(response))
# except:
#     print("error")

