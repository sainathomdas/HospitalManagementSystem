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
    

def insert_logins(values):
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into logins(username, password, role) values({});".format(values);
    try:
        cur.execute(sql)
        return True
    except:
        return False
    conn.commit()
    conn.close()
    

def read_logins(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "select * from logins where {};".format(condition)
    try:
        cur.execute(sql)
    except:
        return False
    rows = cur.fetchall()

    conn.commit()
    conn.close()
    return rows
    

def update_logins(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update logins set {} where {};".format(values, condition)
    
    try:
        cur.execute(sql)
    except:
        return False
    conn.commit()
    conn.close()
    

def delete_logins(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  logins  where {};".format(condition)
    
    try:
        cur.execute(sql)
    except:
        return False
    conn.commit()
    conn.close()
