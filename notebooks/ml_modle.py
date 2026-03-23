# ============================================
# ML MODEL - Travel Budget Prediction
# ============================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

print("=" * 60)
print("TRAVEL BUDGET PREDICTION - ML MODEL")
print("=" * 60)

# Load data
csv_path = r'C:\Users\omaram\OneDrive\Desktop\travel-planner\data\countries.csv'
df = pd.read_csv(csv_path)

print(f"\n✅ Loaded {len(df)} countries")

# Create target: Total cost for 7 days, 2 people
days = 7
people = 2

df['total_cost'] = (
    df['flight_cost_inr'] +
    (df['hotel_per_day_inr'] * days) +
    (df['food_per_day_inr'] * days) +
    (df['local_transport_inr'] * days) +
    df['visa_fee_inr']
) * people

# Encode categorical features
le_continent = LabelEncoder()
df['continent_code'] = le_continent.fit_transform(df['continent'])

# Select features
features = ['flight_cost_inr', 'hotel_per_day_inr', 'food_per_day_inr', 
            'local_transport_inr', 'visa_fee_inr', 'safety_rating', 
            'temperature_c', 'continent_code']

X = df[features]
y = df['total_cost']

print(f"\n📊 Features: {features}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"\n📊 Model Performance:")
print(f"   R² Score: {r2:.4f} ({r2*100:.1f}%)")
print(f"   RMSE: ₹{rmse:,.0f}")

# Feature importance
importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n📊 Feature Importance:")
for i, row in importance.iterrows():
    print(f"   {row['feature']:25}: {row['importance']:.4f}")

# Save model
os.makedirs('models', exist_ok=True)
joblib.dump(model, r'C:\Users\omaram\OneDrive\Desktop\travel-planner\models\budget_predictor.pkl')
joblib.dump(scaler, r'C:\Users\omaram\OneDrive\Desktop\travel-planner\models\scaler.pkl')
joblib.dump(le_continent, r'C:\Users\omaram\OneDrive\Desktop\travel-planner\models\label_continent.pkl')

print(f"\n✅ Model saved to: models/budget_predictor.pkl")
print("\n" + "=" * 60)
print("ML MODEL TRAINING COMPLETE!")
print("=" * 60)