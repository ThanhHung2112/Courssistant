import db_config
from sqlalchemy import create_engine, text
import time
from llama_index.llms.ollama import Ollama
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            db_config.db_user, db_config.db_password, db_config.db_host, db_config.db_port, db_config.db_name
        )
    )
def main():
    llm = Ollama(model="duckdb-nsql", request_timeout=90.0)
    print("Selected Model :: ", llm.model)
    print("=====================")

    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    engine = get_connection()
    db_tables = ["customers","employees",
                 "offices","orderdetails",
                 "orders","payments",          
                 "productlines","products"]

    sql_database = SQLDatabase(engine, include_tables=db_tables)
    query_engine = NLSQLTableQueryEngine(sql_database=sql_database,
                                         tables=db_tables,
                                         llm=llm)
    
    while True:
        print("Enter natural language query")
        query_str = input()
        #query_str = "Find customers with no orders"
        # query_str = "Find number of orders for each status."
        current = time.time()
        response = query_engine.query(query_str)
        print("Query")
        print(response.metadata['sql_query'])
        print(f"Take {(time.time()-current)/60} minute to finish")
        print("=====================")

if __name__ == '__main__':
    main()