from flask import Flask
from sqlalchemy import create_engine, text

db = {
    'user': 'root',
    'password': 'aidan1004',
    'host': 'localhost',
    'port': 3306,
    'database': 'fbBot2'
}

DB_URL = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
EMAIL = 'macqueen01@naver.com'
PASSWORD = 'Goldfrog1004!'