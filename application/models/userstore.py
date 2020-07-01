# To store the login timestamps

import sqlite3
from sqlite3 import Error
def create_conn():
    conn = None
    try:
        conn = sqlite3.connect('DATABASE.db')
        return conn
    except Error as e:
        print(e)
    return conn
    
# this function is used to insert records in user_store table
def insert_user_store(values):
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into user_store(username, timestamp) values({});".format(values)
    
    try:
        cur.execute(sql)
    except:
        return False
    conn.commit()
    conn.close()
    
# this function is used to read records from user_store table
# if no argument is passed, this will return all the records avalable in the table
def read_user_store(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "select * from user_store where {};".format(condition)
    
    try:
        cur.execute(sql)
    except:
        return False
    rows = cur.fetchall()
    
    conn.commit()
    conn.close()
    return rows
    
# this function is used to update records in user_store table based on the condition provided as an arugument
def update_user_store(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update user_store set {} where {};".format(values, condition)
    
    try:
        cur.execute(sql)
    except:
        return False
    conn.commit()
    conn.close()
    
# this function is used to delete records from user_store table based on the condition provided as an arugument
def delete_user_store(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  user_store  where {};".format(condition)
    try:
        cur.execute(sql)
    except:
        return False
    conn.commit()
    conn.close()
