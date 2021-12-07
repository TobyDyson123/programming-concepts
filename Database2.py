import sqlite3
conn = sqlite3.connect("accounts.db")
cur = conn.cursor()

def check_if_user_exists(username, password):
    sql = "SELECT * FROM Users WHERE username = ? AND password = ?"
    cur.execute(sql,(username,password))
    row = cur.fetchall()
    if row:
        return True
    else:
        return False

def check_if_name_taken(username):
    sql = "SELECT * FROM Users WHERE username = ?"
    cur.execute(sql, (username,))
    row = cur.fetchall()
    if row:
        return True
    else:
        return False

def add_details_to_database(username, password):
    sql = "INSERT INTO Users(username, password) VALUES (?, ?)"
    cur.execute(sql, (username,password))
    conn.commit()