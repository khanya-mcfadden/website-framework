from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Ensure the table is created when the app starts
def init_db():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    # Create the users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

# Initialize the database when the app starts
def initialize():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            return "Please fill out all fields", 400  # Simple error handling

        # Insert user into database
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        try:
            # Insert the user
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, password))
            connection.commit()
        except sqlite3.IntegrityError:
            return "User already exists or email is already registered.", 400
        finally:
            connection.close()

        # Redirect to confirmation page
        return redirect('/confirm')
    
    return render_template('register.html')

@app.route('/confirm')
def confirm():
    return render_template('confirm.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the user exists in the database
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        connection.close()

        if user:
            session['username'] = username  # Store username in session
            return redirect(url_for('profile'))
        else:
            return "Invalid username or password", 400

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        return render_template('profile.html', username=username)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    initialize()  # Ensure the database is initialized before running the app
    app.run(debug=True)