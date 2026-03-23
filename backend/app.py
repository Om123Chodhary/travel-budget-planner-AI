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
    return render_template('index.html')


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
    name   = request.form['name']
    budget = float(request.form['budget'])
    days   = int(request.form['days'])
    people = int(request.form['people'])

    per_day    = round(budget / days)
    per_person = round(budget / people)

    if budget >= 200000:
        destination = "International — Europe/Japan/USA"
    elif budget >= 80000:
        destination = "International Asia — Thailand/Dubai/Nepal"
    elif budget >= 30000:
        destination = "Domestic Premium — Goa/Kashmir/Manali"
    else:
        destination = "Domestic Budget — Nearby states"

    return render_template('result.html',
        name=name,
        budget=f"{budget:,.0f}",
        per_day=f"{per_day:,}",
        per_person=f"{per_person:,}",
        destination=destination
    )


# ============================================
# SERVER START
# ============================================
if __name__ == '__main__':
    app.run(debug=True)