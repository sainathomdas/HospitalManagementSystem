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

# this function is used to insert records in patient_diagnostics table
def insert_patient_diagnostics(values):
    print(values)
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into patient_diagnostics(pid,tid) values({});".format(values);

    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    
# this function is used to read records from patient_diagnostics table
# if no argument is passed, this will return all the records avalable in the table
def read_patient_diagnostics(pid):
    conn = create_conn()
    cur = conn.cursor()
    sql = f"SELECT d.name, d.charge FROM diagnostics d, patient_diagnostics p WHERE p.pid={pid} and p.tid=d.id"

    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows
    
# this function is used to update records in patient_diagnostics table based on the condition provided as an arugument
def update_patient_diagnostics(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update patient_diagnostics set {} where {};".format(values, condition)

    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    
# this function is used to delete records from patient_diagnostics table based on the condition provided as an arugument
def delete_patient_diagnostics(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  patient_diagnostics  where {};".format(condition)

    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
        return False
    conn.commit()
    conn.close()
    return True
