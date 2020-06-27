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
    

def insert_diagnostics(values):
    print(values)
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into diagnostics(id, name,charge) values({});".format(values);
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    

def read_diagnostics(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "select * from diagnostics where {};".format(condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows
    

def update_diagnostics(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update diagnostics set {} where {};".format(values, condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    

def delete_diagnostics(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  diagnostics  where {};".format(condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()

def getTestsByName(tname):
    conn = create_conn()
    cur = conn.cursor()
    sql = f"select * from diagnostics where name='{tname}';"
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows