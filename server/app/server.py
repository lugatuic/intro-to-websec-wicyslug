from flask import Flask, request, render_template, redirect, make_response
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("username")

    # SQL Injection Vulnerability
    # TODO: SQLite connection

    response = make_response(redirect("/dashboard"))
    response.set_cookie("session", username) # Insecure session management
    return response

@app.route("/dashboard")
def dashboard():
    user = request.cookies.get("session")
    return render_template("dashboard.html", username=user)

if __name__ == '__main__':
    # host = 0.0.0.0
    # "Bind to all interfaces"
    # Port 80 is default for HTTP services anyhow
    app.run(host="0.0.0.0", port=80)
