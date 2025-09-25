import sqlite3
import random

if __name__ == '__main__':
    f_rockyou = open("rockyou.txt", "r", encoding="latin-1")
    rockyou = f_rockyou.readlines()

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    f_usernames = open("usernames.txt", "r")
    usernames = f_usernames.readlines()

    SQL = "INSERT INTO users (username, password) VALUES (?,?);"

    for username in usernames:
        password = rockyou[random.randint(1,14344391)].strip()
        result = cursor.execute(SQL, [username.strip(), password])
        connection.commit()
