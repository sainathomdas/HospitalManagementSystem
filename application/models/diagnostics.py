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
    
# this function is used to insert records in diagnostics table
def insert_diagnostics(values):
    print(values)
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into diagnostics(id, name,charge) values({});".format(values)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    
# this function is used to read records from diagnostics table
# if no argument is passed, this will return all the records avalable in the table
def read_diagnostics(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "select * from diagnostics where {};".format(condition)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows
    
# this function is used to update records in diagnostics table based on the condition provided as an arugument
def update_diagnostics(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update diagnostics set {} where {};".format(values, condition)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    
# this function is used to delete records from diagnostics table based on the condition provided as an arugument
def delete_diagnostics(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  diagnostics  where {};".format(condition)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()

# this function is used to get diagnostic test details based on the testname provided as an argument
def getTestsByName(tname):
    conn = create_conn()
    cur = conn.cursor()
    sql = f"select * from diagnostics where name='{tname}';"
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows