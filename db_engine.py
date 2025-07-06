# db_engine.py

import sys
import os
sys.path.append(os.path.dirname(__file__))
from sqlalchemy import create_engine
from config import server, database, username, password

connection_string = (
    f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
)
engine = create_engine(connection_string, fast_executemany=True)