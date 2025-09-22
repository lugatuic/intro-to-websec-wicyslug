import sqlite3
import random

if __name__ == '__main__':
    print("WARNING: This is slow and uneeded.","The Database has been initialized already." ,"Only run if you want to change what is in it.","This is just here for posterity.", sep='\n')
    f = open("rockyou.txt", "r", encoding="latin-1")
    rockyou = f.readlines()

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    SQL = "INSERT INTO users (username, password) VALUES (?,?);"

    for i in range(0, 50):
        username = rockyou[random.randint(1,14344391)].strip()
        password = rockyou[random.randint(1,14344391)].strip()
        result = cursor.execute(SQL, [username, password])
        connection.commit()
