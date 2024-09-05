from flask import Flask
from flask import render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Home Page route
@app.route("/")
def home():
    return render_template("index.html")

# Add User route
@app.route("/register", methods=["GET", "POST"])
def register():
    # Get the input values from the form
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    # Connect to the SQLite database
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()

    # Insert the user data into the database
    add_data = data_add(username, email, password)
    if add_data == True:
        return redirect("/confirm")
    else:
        return redirect("/")

    return redirect("/confirm")
def data_add(username, email, password):
    creation_date = datetime.datetime.now()
    # Connect to the SQLite database
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "insert into users (username, email, password, creation_date) values (?, ?, ?, ?)"
    cursor.execute(query, (username, email, password, creation_date))
    conn.commit()
    conn.close()

    return True
@app.route("/confirm")
def confirm():
    return render_template("confirm.html")

@app.route("/login", methods=["POST"])
def login():
    # Login logic here
    pass

if __name__ == "__main__":
    app.run(debug=True)