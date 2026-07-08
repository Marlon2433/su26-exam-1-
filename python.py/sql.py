import mysql.connector
from mysql.connector import Error


def DBConnection(hname, uname, passd, dbname):
    con = None
    try:
        con = mysql.connector.connect(
            host=hname,
            user=uname,
            password=passd,
            database=dbname
        )
        print("DB connection successful")
    except Error as e:
        print("Error is:", e)
    return con


def execute_read_query(con, query, params=None):
    cursor = con.cursor(dictionary=True)
    allrows = None
    try:
        cursor.execute(query, params or ())
        allrows = cursor.fetchall()
        return allrows
    except Error as e:
        print("Error is:", e)


def execute_query(con, query, params=None):
    cursor = con.cursor()
    try:
        cursor.execute(query, params or ())
        con.commit()
        print("DB is updated")
    except Error as e:
        print("Error is:", e)