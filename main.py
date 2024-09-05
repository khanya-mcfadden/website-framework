from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Initialize Flask app
app = Flask(__name__)

# Function to initialize and create Users table if it doesn't exist
def init_db():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        Id INTEGER PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255)
    );
    ''')

    connection.commit()
    connection.close()

# Route to list all users
@app.route("/")
def index():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()

    connection.close()

    return render_template("index.html", users=users)

# Route to register a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        try:
            # Insert user into the database
            cursor.execute("INSERT INTO Users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            connection.commit()

            print(f"User {username} added successfully!")  # Debugging print statement

        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")  # Log any potential errors (like unique constraint violation)
            return "Username or Email already exists!"

        finally:
            connection.close()

        # Redirect to confirmation page
        return redirect(url_for("confirm_account"))

    return render_template("register.html")

# Route to confirm account creation
@app.route("/confirm")
def confirm_account():
    return render_template("confirm.html")

# Route to delete a user by ID
@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Users WHERE Id = ?", (user_id,))
    connection.commit()
    connection.close()

    return redirect(url_for("index"))

# Route to test redirection
@app.route("/test_confirm")
def test_confirm():
    return redirect(url_for("confirm_account"))

# Run the Flask app
if __name__ == "__main__":
    # Initialize the database when the app starts
    init_db()
    app.run(debug=True)
