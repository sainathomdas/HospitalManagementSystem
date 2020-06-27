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


medicine_table = """CREATE TABLE IF NOT EXISTS medicine (
                                    mid integer PRIMARY KEY,
                                    name text NOT NULL,
                                    quantity integer NOT NULL,
                                    rate integer NOT NULL
                                );"""

medicines_issued_table = """CREATE TABLE IF NOT EXISTS medicines_issued (
                                    pid integer NOT NULL,
                                    mid text NOT NULL,
                                    medicine text NOT NULL,
                                    quantity integer NOT NULL,
                                    rate integer NOT NULL,
                                    amount integer NOT NULL,
                                    FOREIGN KEY (pid) REFERENCES patient(pid),
                                    FOREIGN KEY (mid) REFERENCES medicine(mid)
                                );"""

diagnostics_table = """CREATE TABLE IF NOT EXISTS diagnostics (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    charge integer NOT NULL
                                );"""
patient_diagnostics_table = """CREATE TABLE IF NOT EXISTS patient_diagnostics (
                                    pid integer NOT NULL,
                                    tid integet NOT NULL,
                                    FOREIGN KEY (pid) REFERENCES patient(pid),
                                    FOREIGN KEY (tid) REFERENCES diagnostics(id)
                                );"""
                        
conn = create_connection(db_file)

if conn is not None:
    create_table(conn, login_table)
    create_table(conn, user_store_table)
    create_table(conn, patient_table)
    create_table(conn, medicine_table)    
    create_table(conn, medicines_issued_table)
    create_table(conn, diagnostics_table)
    create_table(conn, patient_diagnostics_table)
else:
    print("Error! cannot create the database connection.")
conn.close()

from application.routes import route
