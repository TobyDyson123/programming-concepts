import sqlite3
con = sqlite3.connect("accounts.db")
cur = con.cursor()

def check_if_user_exists(username, password):
    sql = "SELECT * FROM Users WHERE username = ? AND password = ?"
    cur.execute(sql,(username,password))
    row = cur.fetchall()
    if row:
        return True
    else:
        return False