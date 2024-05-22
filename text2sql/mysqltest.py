import db_config
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

p = subprocess.Popen("ollama run duckdb-nsql",
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True)
print(create_table_query)

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
    promt_input = schema + question + "(give me all information)"
    out, _ = p.communicate(input=promt_input.encode())
    final_query = out.decode('utf-8').strip()    
    final_query = final_query.split('\n', 1)[0].strip()
    print(f'get query {final_query} in {time.time() -  current}')
    return final_query

while True:
    question = input("query : ")
    executable_query = QnAWithDuck(question, create_table_query)
    print(executable_query)
    try:
        df = pd.read_sql_query(sql = text(executable_query), con = engine.connect())
        print(df)
        df.to_csv("text.csv")
        agent = Agent(df)
        agent.train(docs="He is the highest")

        response = agent.chat(question + "answer with text or dataframe")
        print(response)
        print(type(response))
    except:
        print("an error orcur")
        
   
