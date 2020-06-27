from flask import Flask
from config import Config
import sqlite3
from sqlite3 import Error

app = Flask(__name__,template_folder = 'templates', static_folder= 'static')

app.config.from_object(Config)

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

db_file = 'DATABASE.db'

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

login_table = """CREATE TABLE IF NOT EXISTS logins (
	username text PRIMARY KEY,
	password text NOT NULL,
	role text NOT NULL
);"""

user_store_table = """CREATE TABLE IF NOT EXISTS user_store (
                                    username text NOT NULL,
                                    timestamp text NOT NULL,
                                    FOREIGN KEY (username) REFERENCES login(username)
                                );"""


patient_table = """CREATE TABLE IF NOT EXISTS patient (
                                    pid integer PRIMARY KEY,
                                    ssnid integer NOT NULL,
                                    name text NOT NULL,
                                    age integer NOT NULL,
                                    dateOfAdmission text NOT NULL,
                                    typeOfBed text NOT NULL,
                                    address text,
                                    state text,
                                    city text,
                                    status text
                                );"""
                        
conn = create_connection(db_file)

if conn is not None:
    create_table(conn, login_table)
    create_table(conn, user_store_table)
    create_table(conn, patient_table)
else:
    print("Error! cannot create the database connection.")
conn.close()

from application.routes import route
