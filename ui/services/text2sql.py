from sqlalchemy import create_engine, text
import os
import subprocess
import time
from subprocess import Popen, PIPE
import re
import pandas as pd
from pandasai import Agent
from pandasai.llm import OpenAI

def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            "root", "", "localhost", "3306", "duck_demo"
        )
    )

def table_schema(table_name, engine):
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

    return create_table_query

# p = subprocess.Popen("ollama run duckdb-nsql",
#                     stdin=subprocess.PIPE,
#                     stdout=subprocess.PIPE,
#                     stderr=subprocess.PIPE,
#                     shell=True)

# os.environ["PANDASAI_API_KEY"] = "$2a$10$lwbP.akrhl.4fXNcDF/oQu5jcUArQwhXCXHNmcoTIYDQAsWEGeHn6"


# llm = OpenAI(
#     api_token="sk-proj-R3zUuZVlUot3lkumt10LT3BlbkFJkYOT041i5sCtoqxHswr4",
# )

def QnAWithDuck(question, schema):
    current = time.time()
    p = subprocess.Popen("ollama run duckdb-nsql",
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True)
    promt_input = schema + question + "give me all field of query result"
    print("ducking")
    out, _ = p.communicate(input=promt_input.encode())
    final_query = out.decode('utf-8').strip()    
    final_query = final_query.split('\n', 1)[0].strip()
    print(f'get query {final_query} in {time.time() -  current}')
    return final_query

def QnAWithPanda(df, question):
    os.environ["PANDASAI_API_KEY"] = "$2a$10$lwbP.akrhl.4fXNcDF/oQu5jcUArQwhXCXHNmcoTIYDQAsWEGeHn6"
    agent = Agent(df)
    print("training pandas")
    agent.train(docs="He is the highest")
    print("panding")
    response = agent.chat(question)
    print(response)
    print(type(response))
    response_text = ""

    if isinstance(response, pd.DataFrame):
        response_text = "here is the result"
    elif isinstance(response, str):
        if "Request failed" in response:
            response_text = "hehe, guess what ?"
        else:
            response_text = response
    elif isinstance(response, int):
        response_text = "the number is " + str(response)
    else:
        response_text = "hehe, guess what ?"
    return response_text
