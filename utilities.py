import json
import os

import psycopg2
from dotenv import load_dotenv

def write_to_file(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f)

def read_from_file(file_name):
    with open(file_name, "r") as f:
        return json.load(f)
    
def get_database_connection():
    load_dotenv()
    password = os.getenv("DB_PASSWORD")
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password=password,
    )
    return conn