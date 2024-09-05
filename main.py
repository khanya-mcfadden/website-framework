from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Initialize Flask app
app = Flask(__name__)


# Function to initialize and create Users table if it doesn't exist
def init_db():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # Create Users table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Users (
        Id INTEGER PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255)
    );
    """
    )

    connection.commit()
    connection.close()


# Initialize the database when the Flask app starts
@app.before_first_request
def initialize_database():
    init_db()


# Route to list all users
@app.route("/")
def index():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()

    connection.close()

    return render_template("index.html", users=users)


# Route to add a new user
@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO Users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            # Handle the case where username or email is not unique
            return "Username or Email already exists!"

        connection.close()

        return redirect(url_for("index"))

    return render_template("add_user.html")


# Route to delete a user by ID
@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Users WHERE Id = ?", (user_id,))
    connection.commit()
    connection.close()

    return redirect(url_for("index"))


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
