import pandas as pd
import streamlit as st

df = pd.read_csv("text.csv")


st.title("Test GRID")

df_top_15 = df.head(15)

data_array = df_top_15.values.reshape((5, 3, -1))  

card_height = 300

for row in data_array:
    cols = st.columns(3)  
    for col, item in zip(cols, row):  
        col.markdown(f"""
        <div style="border: 2px solid #4CAF50; margin: 5px; padding: 10px; border-radius: 10px; height: {card_height}px;">
            <h2 style="color: #4CAF50;">{item[0]}</h2>  <!-- Assuming the first column is contactLastName -->
            <p><strong>contactFirstName:</strong> {item[1]}</p>  <!-- Assuming the second column is contactFirstName -->
            <p><strong>phone:</strong> {item[2]}</p>  <!-- Assuming the third column is phone -->
        </div>
        """, unsafe_allow_html=True)