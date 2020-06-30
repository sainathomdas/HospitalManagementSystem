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

def insert_patient_diagnostics(values):
    print(values)
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into patient_diagnostics(pid,tid) values({});".format(values);
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    

def read_patient_diagnostics(pid):
    conn = create_conn()
    cur = conn.cursor()
    sql = f"SELECT d.name, d.charge FROM diagnostics d, patient_diagnostics p WHERE p.pid={pid} and p.tid=d.id"
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows
    

def update_patient_diagnostics(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update patient_diagnostics set {} where {};".format(values, condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    

def delete_patient_diagnostics(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  patient_diagnostics  where {};".format(condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
        return False
    conn.commit()
    conn.close()
    return True
