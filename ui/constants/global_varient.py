import pandas as pd

execute_whisper = False

def set_execute_whisper(value):
    global execute_whisper
    execute_whisper = value

def get_execute_whisper():
    return execute_whisper


df_display = pd.read_csv("assistant/data/courssistant_main.csv")

def set_df_display(value):
    global df_display
    df_display = value

def get_df_display():
    return df_display
