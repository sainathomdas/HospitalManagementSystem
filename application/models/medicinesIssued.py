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


def insert_medicines_issued(values):
    print(values)
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into medicines_issued(pid, medicine,quantity,rate, amount) values({});".format(values);
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    

def read_medicines_issued(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "select * from medicines_issued where {};".format(condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows
    

def update_medicines_issued(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update medicines_issued set {} where {};".format(values, condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
        return False
    conn.commit()
    conn.close()
    return True
    

def delete_medicines_issued(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  medicines_issued  where {};".format(condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
