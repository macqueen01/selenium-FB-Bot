from flask import Flask
from sqlalchemy import create_engine, text

db = {
    'user': 'root',
    'password': 'aidan1004',
    'host': 'localhost',
    'port': 3306,
    'database': 'fbBot2'
}

DB_URL = "mysql://b715fbc9127dd4:fcdbcf19@us-cdbr-east-04.cleardb.com/heroku_59572923001aaae"
EMAIL = 'macqueen01@naver.com'
PASSWORD = 'Goldfrog1004!'