from pandasai import SmartDataframe
import pandas as pd
# df = pd.DataFrame({
#     "country": [
#         "United States",
#         "United Kingdom",
#         "France",
#         "Germany",
#         "Italy",
#         "Spain",
#         "Canada",
#         "Australia",
#         "Japan",
#         "China",
#     ],
#     "gdp": [
#         19294482071552,
#         2891615567872,
#         2411255037952,
#         3435817336832,
#         1745433788416,
#         1181205135360,
#         1607402389504,
#         1490967855104,
#         4380756541440,
#         14631844184064,
#     ],
#     "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.4, 7.23, 7.22, 5.87, 5.12],
# })

import os

# os.environ["PANDASAI_API_KEY"] = ""
from pandasai import Agent
from pandasai.llm import OpenAI

llm = OpenAI(
    api_token="",
)
df = pd.read_csv("text.csv")
agent = Agent(df)
agent.train(docs="He is the highest")

response = agent.chat("Who is the customer with the highest credit limit?")
print(response)