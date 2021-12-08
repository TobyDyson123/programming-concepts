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

def add_user_score_to_database(username, gold, time):
    sql = "SELECT userID FROM Users WHERE username LIKE ?"
    cur.execute(sql, (username,))
    rows = cur.fetchall()
    for row in rows:
        user_id = row[0]
    conn.commit()
    sql = "INSERT INTO Scores(userID, gold, timeTaken) VALUES (?, ?, ?)"
    cur.execute(sql, (user_id, gold, time))
    conn.commit()

def get_all_highscores_by_gold():
    sql = "SELECT U.username, S.gold, S.timeTaken FROM Scores AS S JOIN Users AS U ON S.userID = U.userID ORDER BY S.gold DESC"
    cur.execute(sql)
    row = cur.fetchall()
    return row

def get_all_highscores_by_time():
    sql = "SELECT U.username, S.gold, S.timeTaken FROM Scores AS S JOIN Users AS U ON S.userID = U.userID ORDER BY S.timeTaken ASC"
    cur.execute(sql)
    row = cur.fetchall()
    return row