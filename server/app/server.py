from flask import Flask, request, render_template, redirect, make_response
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Connect to database
    dbConn = sqlite3.connect("app/users.db")
    cursor = dbConn.cursor()
    # SQL Injection Vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = cursor.execute(query).fetchone()

    if result:
        response = make_response(redirect("/dashboard"))
        response.set_cookie("session", username)
        return response
    else:
        return f"Invalid credentials. <a href='/'>Try again</a><br/><p>{query}</p>"

@app.route("/dashboard")
def dashboard():
    user = request.cookies.get("session")
    return render_template("dashboard.html", username=user)

if __name__ == '__main__':
    # host = 0.0.0.0
    # "Bind to all interfaces"
    # Port 80 is default for HTTP services anyhow
    app.run(host="0.0.0.0", port=80)
