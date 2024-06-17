from sqlalchemy import create_engine, text
import os
import subprocess
import time
from subprocess import Popen, PIPE
import random
import numpy as np
import pandas as pd
from pandasai import Agent
from pandasai.llm import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    print("Running ollama query generate model")
    out, _ = p.communicate(input=promt_input.encode())
    final_query = out.decode('utf-8').strip()    
    final_query = final_query.split('\n', 1)[0].strip()
    print(f'Get Query {final_query} In {time.time() -  current}')
    return final_query

def QnAWithPanda(df, question):

    api_key = os.getenv("PANDASAI_KEY")
    if not api_key:
        raise ValueError("PANDASAI_KEY is not set in the environment variables.")
    os.environ["PANDASAI_API_KEY"] = api_key

    agent = Agent(df)
    print("Training pandas")

    response_texts = [
        "Here is your output.",
        "This is what you've got.",
        "Here's the result you asked for."
    ]

    error_texts = [
        "Oops! Something went wrong while trying to answer, here is your output.",
        "Sorry, we encountered an error, here is your output",
        "Hmm, it seems there was an error, here is your output"
    ]

    while True:
        try:
            agent.train(docs="He is the highest")
            print("Pandas training completed")
            break
        except Exception as e:
            print(f"Error during training: {e}. Retrying...")

    while True:
        try:
            response = agent.chat(question)
            # if "Request failed" in response:
            #     raise ValueError("Request failed")
            break
        except Exception as e:
            print(f"Error during chat: {e}. Retrying...")

    if isinstance(response, pd.DataFrame):
        response_text = random.choice(response_texts)
    elif isinstance(response, str):
        if "Request failed" in response:
            response_text = random.choice(error_texts)
        else:
            response_text = response
    elif isinstance(response, (int, np.int64, np.integer)):
        response_text = f"The number of items to search is {str(response)}"
    else:
        response_text = random.choice(error_texts)

    return response_text
    
