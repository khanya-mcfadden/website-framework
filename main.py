from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def Contact():
    return render_template('ContactPage.html')

@app.route('/Booking')
def Booking():
    return render_template('BookingSeats.html')

@app.route('/ordering')
def ordering():
    return render_template('Ordering.html')
@app.route('/testing')
def testing(): 
    return render_template('ordering.html')
if __name__ == '__main__':
    app.run(debug=True)