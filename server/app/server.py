from flask import Flask, request, render_template, redirect, make_response, Response
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

    post = post.replace("'", "\"")

    register_SQL = "INSERT INTO postIDs VALUES (NULL, ?);"

    # Register post w/ postIDs table
    cursor.execute(register_SQL, [user])
    postID = cursor.lastrowid
    dbConn.commit()
    # Last generated rowID = postID!

    # Save post in SQL
    # Purposely unsanitized: Stored XSS Vuln
    post_SQL = f"INSERT INTO posts VALUES ({postID}, '{user}', '{post}');"
    cursor.execute(post_SQL)
    dbConn.commit()

# Get all the posts from a given user
def get_posts(user):
    dbConn = sqlite3.connect(DATABASE)
    cursor = dbConn.cursor()

    # We're already making things inesecure, so to get all recent posts, we can just:
    if user == "recent":
        postID_SQL = "SELECT postID FROM postIDs ORDER BY postID DESC LIMIT 10;"
        result = cursor.execute(postID_SQL)
    # Select the 5 most recent postIDs from a given user.
    else:
        postID_SQL = "SELECT postID FROM postIDs WHERE user = ? ORDER BY postID DESC LIMIT 5;"
        result = cursor.execute(postID_SQL, [user])
    postIDs = result.fetchall()

    posts = []
    # user, post
    fetch_SQL = "SELECT user, post FROM posts WHERE postID = ?;"
    
    if len(postIDs) == 0:
        return None
    else:
        for i in range(0, len(postIDs)):
            result = cursor.execute(fetch_SQL, [postIDs[i][0]])
            post = result.fetchone()
            posts.append(post)
        return posts 

# Given a string representation of a post, return its HTML representation
def build_post(user, post_raw):
    post = "<div class=\"post\">"
    # User Tag
    post += f"<b>@{user}</b><br>" 
    post += f"{post_raw}"
    post += "</div>"
    return post

# Given a list of posts as strings, build their html representations
# user, post
def build_posts(posts_raw):
    posts = []
    if posts_raw == None or len(posts_raw) == 0:
        return None
    for post in posts_raw:
        posts.append(build_post(post[0], post[1]))
    return posts

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
    user = request.args.get('username')
    # Get all the posts into a list for awesome templating :)
    if user == "" or user == None:
        user = "recent"
    posts_raw = get_posts(user)
    # if posts_raw == None:
    #     return render_template("search.html", username=user)
    # for i in range(0,5):
    #     if(request.cookies.get(f"post_{i}") != None):
    #        posts.append(request.cookies.get(f"post_{i}"))
    posts = build_posts(posts_raw)
    if posts == None:
        posts = []
    # Flask templating is actually intelligent and stops you from introducing XSS vulns. Time to completely undo their hard work :D
    # Idea is to pass each post's html through a list and building them ourselves so we don't sanitize input in the slightest :D
    
    # Reflective XSS vulnerability
    # I mean awesome dynamic title generation that is totally safe :)
    title = f"<title>{user}</title>"
    site = title + render_template("search.html", username=user)
    for post in posts:
        site += post
    return site
    # GET = Get a given post

# TODO: Stored XSS - User Posts
@app.route("/post", methods=["POST"])
def post():
    user = request.cookies.get("session")
    post = request.form.get("post")
    post.replace("'", "\"")
    make_post(user, post)
    return make_response(redirect("/dashboard"))


if __name__ == '__main__':
    # host = 0.0.0.0
    # "Bind to all interfaces"
    # Port 80 is default for HTTP services anyhow
    app.run(host=IP, port=80)
