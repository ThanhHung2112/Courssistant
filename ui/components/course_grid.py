from services.text2sql import get_connection, QnAWithDuck, QnAWithPanda, table_schema
import streamlit as st
import pandas as pd
from sqlalchemy import text


def display_course_grid(df):
    card_height = 400

    num_columns = 3
    num_rows = len(df)
    
    rows = [df.iloc[i:i + num_columns] for i in range(0, num_rows, num_columns)]
    # Define a dictionary to map specialized fields to image URLs
    specialized_to_img = {
        "Arts and Humanities": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0usqz59pLW_JtU7y9Q0oLQlg41d3prf_Cig&s",
        "Business": "https://i.ytimg.com/vi/T3l51Psce3c/hq720.jpg?sqp=-oaymwEXCK4FEIIDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLCrv13tuDIeoFpS2lgoovFGblgEbw",
        "Information Technology": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8crcAa-v09etPMRk2Vh36xujNDVg6cdVBNgP237Yc_w11Gq5-RSxG8OXNF-Z1sJLNGm4&usqp=CAU",
        "Physical Science and Engineering": "https://online.stanford.edu/sites/default/files/styles/widescreen_tiny/public/2018-03/statisticalmethodsinengineeringphysicalsciences_stats110.jpg?h=66807ab2&itok=WB8u3wVd",
        "Health": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKZV0wIBeCLosu94-ACwliQWEHmccPIrFE87KYKeWHsM-Y2yuow-qaVdBr1LYQGdkjWHE&usqp=CAU",
        "Data Science": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2bj684ua5xtkrYixfQ4vm9sF4k9qP9vT3cPNvUTkH-cxDo1JW9gmp9LKJBaYKz0OQDNs&usqp=CAU",
        "Computer Science": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ6HsC6k3h5C2pzM9GYlnyX2N9ziSWiE2fqgA&s"
    }

    # Default image URL
    default_img_scr = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQN9mLqVjKSSwvlY_o4pTeOKY2oSpbQYDFcjw&s"

    for row in rows:
        cols = st.columns(num_columns)
        for col, (index, item) in zip(cols, row.iterrows()):

            img_scr = specialized_to_img.get(item['Specialized'], default_img_scr)
            name = item['CourseName'] if len(item['CourseName']) <= 50 else item['CourseName'][:42] + '...'
            col.markdown(f"""
            <div style="margin-bottom: 20px;">
                <div style="border: 2px solid #000; padding: 10px; border-radius: 10px; background-color: #fff; height: {card_height}px;">
                    <h5 style="min-height: 85px; max-height: 85px; color: #000;">{name}</h2>
                    <img src={img_scr}, style="width:200px; min-height:150px">
                    <p style="color: #000;"><strong>Difficulty Level:</strong> {item['DifficultyLevel']}</p>
                    <p style="color: #000;"><strong>Description:</strong> {item['CourseDescription'][:80]} ...</p>
                </div>
            </div>
            """, unsafe_allow_html=True)


def QnA_SQL(userInput):
    engineSQL = get_connection()
    create_table_query = table_schema("courses", engineSQL)
    queryExecutable = QnAWithDuck(userInput, create_table_query)
    df = pd.read_sql_query(sql = text(queryExecutable), con = engineSQL.connect())
    print(df)
    df_pd = df.drop(columns=['CourseURL'])
    response = QnAWithPanda(df_pd[:100], userInput)
    print(response)
    # df.to_csv("../df_display/main_screen.csv")
    return df, response

