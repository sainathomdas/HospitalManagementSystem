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

# this function is used to insert records in patient table
def insert_patient(values):
    print(values)
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into patient(pid, ssnid,name,age, dateOfAdmission, typeOfBed, address, city,state,status) values({});".format(values)
    try:
        cur.execute(sql)
    except sqlite3.Error as er:
        print("Something Went wrong - insert")
        print(er)
        return False
    conn.commit()
    conn.close()
    return True    


# this function is used to read records from patient table
# if no argument is passed, this will return all the records avalable in the table
def read_patient(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "select * from patient where {};".format(condition)
    try:
        cur.execute(sql)
    except sqlite3.Error as er:
        print("Something Went wrong")
        print(er)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows    

# this function is used to update records in patient table based on the condition provided as an arugument
def update_patient(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update patient set {} where {};".format(values, condition)

    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
        return False
    conn.commit()
    conn.close()
    return True    

# this function is used to delete records from patient table based on the condition provided as an arugument
def delete_patient(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  patient  where {};".format(condition)

    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
        return False
    conn.commit()
    conn.close()
    return True

# used for retrieving the last row from the patients table to create a new patient id
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