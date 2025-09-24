from flask import Flask, request, render_template, redirect, make_response
import sqlite3

app = Flask(__name__)

# Database holding user data
DATABASE = "app/users.db"
# IP to bind to
IP = "0.0.0.0"

# Saves the post to our totally efficient awesome server by:
# Creating an entry in postIDs
# Saving the entry in posts after registration
def make_post(user, post):
    dbConn = sqlite3.connect(DATABASE)
    cursor = dbConn.cursor()

    register_SQL = "INSERT INTO postIDs VALUES (NULL, ?);"

    # Register post w/ postIDs table
    cursor.execute(register_SQL, [user])
    dbConn.commit()
    # Last generated rowID = postID!
    postID = cursor.lastrowid

    # Save post in SQL
    # Purposely unsanitized: Stored XSS Vuln
    post_SQL = f"INSERT INTO posts VALUES ({postID}, '{user}', '{post}');"
    cursor.execute(post_SQL)
    dbConn.commit()

# Get all the posts from a given user
def get_posts(user):
    dbConn = sqlite3.connect(DATABASE)
    cursor = dbConn.cursor()

    # Select the 5 most recent postIDs from a given user.
    postID_SQL = "SELECT postID FROM postIDs WHERE user = ? ORDER BY postID DESC LIMIT 5;"
    result = cursor.execute(postID_SQL, [user])
    postIDs = result.fetchall()

    posts = []
    fetch_SQL = "SELECT post FROM posts WHERE postID = ?;"
    
    response.set_cookie("posts_fetched", len(postIDs))
    for i in range(0, len(postIDs)):
        result = cursor.execute(fetch_SQL, [postIDs[i]])
        response.set_cookie(f"post_{i}", f"{result.fetchone()[0]}")
        posts.append(result.fetchone()[0])

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Connect to database
    dbConn = sqlite3.connect(DATABASE)
    cursor = dbConn.cursor()
    # SQL Injection Vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = cursor.execute(query).fetchone()
    cursor.close()

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

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    # Reflective XSS vulnerability / Potential DOM - XSS
    # I mean awesome dynamic title generation that is totally safe :)
    title = f"<title>{query}</title>"
    return title + render_template("search.html", query=query)

# TODO: Stored XSS - User Posts
@app.route("/post", methods=["POST", "GET"])
def post():
    # POST = User makes a post
    if request.method == 'POST':
        user = request.cookies.get("session")
        post = request.form.get("post")
        make_post(user, post)
        return make_response(redirect("/dashboard"))

    # GET = Get a given post
    if request.method == 'GET':
        username = request.args.get("username")
        get_posts(username)

if __name__ == '__main__':
    # host = 0.0.0.0
    # "Bind to all interfaces"
    # Port 80 is default for HTTP services anyhow
    app.run(host=IP, port=80)
