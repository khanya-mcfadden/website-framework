from flask import Flask, render_template
import sqlite3
connection = sqlite3.connect("user.db")
cursor = connection.cursor()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/ordering")
def ordering():
    return render_template("ordering.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


if __name__ == "__main__":
    app.run(debug=True)
