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
    


def insert_patient(values):
    print(values)
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into patient(pid, ssnid,name,age, dateOfAdmission, typeOfBed, address, city,state,status) values({});".format(values);
    print(sql)
    try:
        cur.execute(sql)
    except sqlite3.Error as er:
        print("Something Went wrong - insert")
        print(er)
        return False
    conn.commit()
    conn.close()
    return True
    

def read_patient(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "select * from patient where {};".format(condition)
    print(sql)
    try:
        cur.execute(sql)
    except sqlite3.Error as er:
        print("Something Went wrong - read")
        print(er)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows
    

def update_patient(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update patient set {} where {};".format(values, condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
        return False
    conn.commit()
    conn.close()
    return True
    

def delete_patient(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  patient  where {};".format(condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
        return False
    conn.commit()
    conn.close()
    return True

def getLastRow():
    conn = create_conn()
    cur = conn.cursor()
    sql = "SELECT * FROM patient ORDER BY pid DESC LIMIT 1;"    
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()    
    conn.commit()
    conn.close()
    return rows
    
