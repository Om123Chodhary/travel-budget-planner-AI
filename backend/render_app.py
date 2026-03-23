from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# ============================================
# CONFIGURATION
# ============================================

app.config['SECRET_KEY'] = 'travel-budget-ai-secret-key-2024'

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "travel_planner.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ============================================
# DATABASE MODELS
# ============================================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviews = db.relationship('Review', backref='author', lazy=True)
    saved_trips = db.relationship('SavedTrip', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SavedTrip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    people = db.Column(db.Integer, nullable=False)
    style = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()

# ============================================
# DATA LOADING
# ============================================

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'countries.csv')

def load_data():
    try:
        df = pd.read_csv(CSV_PATH)
        return df
    except:
        return None

def get_affordable_countries(budget, days, people, style):
    df = load_data()
    if df is None:
        return []
    
    style_multiplier = {'budget': 0.8, 'moderate': 1.0, 'luxury': 1.5}
    multiplier = style_multiplier.get(style, 1.0)
    
    df['flight'] = df['flight_cost_inr']
    df['hotel'] = df['hotel_per_day_inr'] * days * multiplier
    df['food'] = df['food_per_day_inr'] * days * multiplier
    df['transport'] = df['local_transport_inr'] * days
    df['visa'] = df['visa_fee_inr']
    
    df['total_cost'] = (df['flight'] + df['hotel'] + df['food'] + df['transport'] + df['visa']) * people
    
    affordable = df[df['total_cost'] <= budget].copy()
    affordable = affordable.sort_values(['safety_rating', 'total_cost'], ascending=[False, True])
    
    return affordable

# ============================================
# ROUTES
# ============================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('signup'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    saved_trips = SavedTrip.query.filter_by(user_id=current_user.id).order_by(SavedTrip.created_at.desc()).all()
    user_reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).all()
    return render_template('profile.html', saved_trips=saved_trips, user_reviews=user_reviews)

@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    budget = float(request.form['budget'])
    days = int(request.form['days'])
    people = int(request.form['people'])
    style = request.form['style']
    
    per_day = round(budget / days)
    per_person = round(budget / people)
    
    countries_df = get_affordable_countries(budget, days, people, style)
    
    if current_user.is_authenticated:
        saved_trip = SavedTrip(
            user_id=current_user.id,
            budget=budget,
            days=days,
            people=people,
            style=style
        )
        db.session.add(saved_trip)
        db.session.commit()
    
    countries = []
    for _, row in countries_df.head(20).iterrows():
        countries.append({
            'country': row['country'],
            'continent': row['continent'],
            'total_cost': f"{row['total_cost']:,.0f}",
            'flight_cost': f"{row['flight']:,.0f}",
            'hotel_cost': f"{row['hotel']:,.0f}",
            'food_cost': f"{row['food']:,.0f}",
            'transport_cost': f"{row['transport']:,.0f}",
            'visa_cost': f"{row['visa']:,.0f}",
            'best_time': row['best_time'],
            'safety': row['safety_rating'],
            'language': row['language'],
            'temperature': row.get('temperature_c', 'N/A'),
            'weather_icon': row.get('weather_icon', '☀️'),
            'currency': row.get('currency_code', 'INR'),
            'days': days,
            'people': people
        })
    
    total_found = len(countries_df)
    cheapest = countries_df['total_cost'].min() if total_found > 0 else 0
    most_expensive = countries_df['total_cost'].max() if total_found > 0 else 0
    avg_cost = countries_df['total_cost'].mean() if total_found > 0 else 0
    
    return render_template('result.html',
        name=name,
        budget=f"{budget:,.0f}",
        per_day=f"{per_day:,}",
        per_person=f"{per_person:,}",
        countries=countries,
        total_found=total_found,
        cheapest=f"{cheapest:,.0f}",
        most_expensive=f"{most_expensive:,.0f}",
        avg_cost=f"{avg_cost:,.0f}",
        style=style,
        user_logged_in=current_user.is_authenticated
    )

@app.route('/add_review', methods=['POST'])
@login_required
def add_review():
    country = request.form['country']
    rating = int(request.form['rating'])
    comment = request.form['comment']
    
    review = Review(
        country=country,
        rating=rating,
        comment=comment,
        user_id=current_user.id
    )
    db.session.add(review)
    db.session.commit()
    
    flash(f'Thank you! Your review for {country} has been posted.', 'success')
    return redirect(request.referrer or url_for('home'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'Omaram123' and password == '7891424454':
            session['admin_logged_in'] = True
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    users = User.query.all()
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    saved_trips = SavedTrip.query.order_by(SavedTrip.created_at.desc()).all()
    
    return render_template('admin_dashboard.html',
        users=users,
        reviews=reviews,
        saved_trips=saved_trips,
        total_users=len(users),
        total_reviews=len(reviews),
        total_trips=len(saved_trips)
    )

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

# ============================================
# RUN APP
# ============================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)