# ============================================
# Travel Planner - Flask App
# Phase 1 - Pehla Web Server!
# ============================================

from flask import Flask, render_template, request, jsonify

# Flask app banao
# __name__ matlab "is file ka naam use karo"
app = Flask(__name__)


# ---- ROUTE 1: Home Page ----
# Jab browser mein localhost:5000 kholo
@app.route('/')
def home():
    return '''
    <html>
    <head><title>Travel Planner</title></head>
    <body>
        <h1>Budget Based Travel Planner</h1>
        <p>Namaste! Aapka Travel Planner ready hai!</p>
        <a href="/calculator">Calculator kholo</a>
    </body>
    </html>
    '''


# ---- ROUTE 2: Calculator Page ----
# Jab /calculator URL pe jaao
@app.route('/calculator')
def calculator():
    return '''
    <html>
    <head><title>Budget Calculator</title></head>
    <body>
        <h1>Travel Budget Calculator</h1>
        <form action="/result" method="POST">
            <label>Aapka Naam:</label><br>
            <input type="text" name="name"><br><br>

            <label>Budget (Rs mein):</label><br>
            <input type="number" name="budget"><br><br>

            <label>Kitne Din:</label><br>
            <input type="number" name="days"><br><br>

            <label>Kitne Log:</label><br>
            <input type="number" name="people"><br><br>

            <button type="submit">Calculate!</button>
        </form>
    </body>
    </html>
    '''


# ---- ROUTE 3: Result Page ----
# Form submit hone ke baad yahan aata hai
@app.route('/result', methods=['POST'])
def result():
    # Form se data lo
    name   = request.form['name']
    budget = float(request.form['budget'])
    days   = int(request.form['days'])
    people = int(request.form['people'])

    # Calculate karo
    per_day    = budget / days
    per_person = budget / people

    # Destination suggest karo
    if budget >= 200000:
        destination = "International - Europe/Japan/USA"
    elif budget >= 80000:
        destination = "International Asia - Thailand/Dubai/Nepal"
    elif budget >= 30000:
        destination = "Domestic Premium - Goa/Kashmir/Manali"
    else:
        destination = "Domestic Budget - Nearby states"

    return f'''
    <html>
    <head><title>Result</title></head>
    <body>
        <h1>Namaste {name}!</h1>
        <h2>Aapki Travel Detail:</h2>
        <p>Total Budget  : Rs {budget:,.0f}</p>
        <p>Per Day       : Rs {per_day:,.0f}</p>
        <p>Per Person    : Rs {per_person:,.0f}</p>
        <p>Best Option   : {destination}</p>
        <br>
        <a href="/calculator">Wapas jaao</a>
    </body>
    </html>
    '''


# ============================================
# SERVER START
# ============================================
if __name__ == '__main__':
    app.run(debug=True)