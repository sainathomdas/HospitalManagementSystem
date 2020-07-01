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

# this function is used to insert records in medicine table
def insert_medicine(values):
    print(values)
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into medicine(mid, name,quantity,rate) values({});".format(values)

    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    
# this function is used to read records from medicine table
# if no argument is passed, this will return all the records avalable in the table
def read_medicine(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "select * from medicine where {};".format(condition)

    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows
    
# this function is used to update records in medicine table based on the condition provided as an arugument
def update_medicine(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update medicine set {} where {};".format(values, condition)

    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
        return False
    conn.commit()
    conn.close()
    return True
    
# this function is used to delete records from medicine table based on the condition provided as an arugument
def delete_medicine(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  medicine  where {};".format(condition)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
