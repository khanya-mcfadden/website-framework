from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Home')
def Home():
    return render_template('HomePage.html')

@app.route('/contact')
def Contact():
    return render_template('ContactPage.html')

@app.route('/Booking')
def Booking():
    return render_template('BookingSeats.html')

@app.route('/ordering')
def ordering():
    return render_template('Ordering.html')

if __name__ == '__main__':
    app.run()
    app.run(debug=True)