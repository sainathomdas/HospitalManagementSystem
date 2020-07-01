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

# this function is used to insert records in medicines_issued table
def insert_medicines_issued(values):
    print(values)
    conn = create_conn()
    cur = conn.cursor()
    sql = "insert into medicines_issued(pid, mid,medicine,quantity,rate,amount) values({});".format(values);

    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    

# this function is used to read records from medicines_issued table
# if no argument is passed, this will return all the records avalable in the table
def read_medicines_issued(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "select * from medicines_issued where {};".format(condition)

    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows
    
# this function is used to update records in medicines_issued table based on the condition provided as an arugument
def update_medicines_issued(values, condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "update medicines_issued set {} where {};".format(values, condition)

    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    
# this function is used to delete records from medicines_issued table based on the condition provided as an arugument
def delete_medicines_issued(condition="1=1"):
    conn = create_conn()
    cur = conn.cursor()
    sql = "delete from  medicines_issued  where {};".format(condition)

    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
        return False
    conn.commit()
    conn.close()
    return True
