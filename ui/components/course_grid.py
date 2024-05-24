from services.text2sql import get_connection, QnAWithDuck, QnAWithPanda, table_schema
import streamlit as st
import pandas as pd
from sqlalchemy import text


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

def QnA_SQL(userInput):
    engineSQL = get_connection()
    create_table_query = table_schema("customers", engineSQL)
    queryExecutable = QnAWithDuck(userInput, create_table_query)
    df = pd.read_sql_query(sql = text(queryExecutable), con = engineSQL.connect())
    print(df)
    response = QnAWithPanda(df, userInput)
    print(response)
    df.to_csv("df_display.csv")
    return df, response

