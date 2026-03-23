# ============================================
# PHASE 2: DATA ANALYSIS - TRAVEL DATASET
# Complete Analysis with Visualizations
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# For better display
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', 50)

# ============================================
# 1. DATA LOADING
# ============================================

print("=" * 60)
print("TRAVEL DATASET ANALYSIS")
print("=" * 60)

# Load the dataset
csv_path = r'C:\Users\omaram\OneDrive\Desktop\travel-planner\data\countries.csv'
df = pd.read_csv(csv_path)

print(f"\n✅ Dataset Loaded Successfully!")
print(f"📊 Total Countries: {len(df)}")
print(f"📋 Columns: {len(df.columns)}")
print(f"\n📁 Columns: {df.columns.tolist()}")

# ============================================
# 2. BASIC INFORMATION
# ============================================

print("\n" + "=" * 60)
print("2. BASIC INFORMATION")
print("=" * 60)

print("\n📊 First 5 Rows:")
print(df.head())

print("\n📊 Data Types:")
print(df.dtypes)

print("\n📊 Missing Values:")
print(df.isnull().sum())

print("\n📊 Statistical Summary:")
print(df.describe())

# ============================================
# 3. CONTINENT-WISE ANALYSIS
# ============================================

print("\n" + "=" * 60)
print("3. CONTINENT-WISE ANALYSIS")
print("=" * 60)

# Continent count
continent_counts = df['continent'].value_counts()
print("\n🌍 Countries per Continent:")
for continent, count in continent_counts.items():
    print(f"   {continent}: {count} countries")

# Average cost by continent
print("\n💰 Average Costs by Continent:")
continent_avg = df.groupby('continent').agg({
    'flight_cost_inr': 'mean',
    'hotel_per_day_inr': 'mean',
    'food_per_day_inr': 'mean',
    'safety_rating': 'mean'
}).round(2)

print(continent_avg)

# ============================================
# 4. SAFETY RATING ANALYSIS
# ============================================

print("\n" + "=" * 60)
print("4. SAFETY RATING ANALYSIS")
print("=" * 60)

# Safety distribution
print("\n🛡️ Safety Rating Distribution:")
safety_counts = df['safety_rating'].value_counts().sort_index()
for rating, count in safety_counts.items():
    print(f"   Rating {rating}: {count} countries")

# Safest countries
print("\n🌟 Top 10 Safest Countries:")
safest = df.nlargest(10, 'safety_rating')[['country', 'continent', 'safety_rating', 'language']]
print(safest.to_string(index=False))

# Least safe countries
print("\n⚠️ Bottom 10 Safest Countries:")
least_safe = df.nsmallest(10, 'safety_rating')[['country', 'continent', 'safety_rating']]
print(least_safe.to_string(index=False))

# ============================================
# 5. BUDGET FRIENDLY ANALYSIS
# ============================================

print("\n" + "=" * 60)
print("5. BUDGET FRIENDLY ANALYSIS (7 Days, 2 People)")
print("=" * 60)

# Calculate total cost for 7 days, 2 people
days = 7
people = 2

df['total_cost_7days_2p'] = (
    df['flight_cost_inr'] +
    (df['hotel_per_day_inr'] * days) +
    (df['food_per_day_inr'] * days) +
    (df['local_transport_inr'] * days) +
    df['visa_fee_inr']
) * people

# Cheapest countries
print("\n💰 10 Cheapest Countries:")
cheapest = df.nsmallest(10, 'total_cost_7days_2p')[
    ['country', 'continent', 'total_cost_7days_2p', 'safety_rating']
]
for _, row in cheapest.iterrows():
    print(f"   {row['country']:20} | {row['continent']:10} | ₹{row['total_cost_7days_2p']:,.0f} | Safety: {row['safety_rating']}/10")

# Most expensive countries
print("\n👑 10 Most Expensive Countries:")
expensive = df.nlargest(10, 'total_cost_7days_2p')[
    ['country', 'continent', 'total_cost_7days_2p', 'safety_rating']
]
for _, row in expensive.iterrows():
    print(f"   {row['country']:20} | {row['continent']:10} | ₹{row['total_cost_7days_2p']:,.0f} | Safety: {row['safety_rating']}/10")

# ============================================
# 6. BUDGET CATEGORIES
# ============================================

print("\n" + "=" * 60)
print("6. BUDGET CATEGORIES (7 Days, 2 People)")
print("=" * 60)

def budget_category(cost):
    if cost <= 50000:
        return "Budget (₹0-50k)"
    elif cost <= 100000:
        return "Moderate (₹50k-1L)"
    elif cost <= 150000:
        return "Premium (₹1L-1.5L)"
    else:
        return "Luxury (₹1.5L+)"

df['budget_category'] = df['total_cost_7days_2p'].apply(budget_category)

category_counts = df['budget_category'].value_counts()
print("\n📊 Countries by Budget Category:")
for category, count in category_counts.items():
    percentage = (count / len(df)) * 100
    print(f"   {category}: {count} countries ({percentage:.1f}%)")

# Show examples per category
print("\n📌 Examples per Category:")
for category in ['Budget (₹0-50k)', 'Moderate (₹50k-1L)', 'Premium (₹1L-1.5L)', 'Luxury (₹1.5L+)']:
    examples = df[df['budget_category'] == category].head(3)['country'].tolist()
    if examples:
        print(f"   {category}: {', '.join(examples)}")

# ============================================
# 7. SEASONAL ANALYSIS
# ============================================

print("\n" + "=" * 60)
print("7. BEST TIME TO VISIT ANALYSIS")
print("=" * 60)

# Extract season from best_time
def get_season(best_time):
    if pd.isna(best_time):
        return "Unknown"
    if 'Jan' in best_time or 'Feb' in best_time:
        return "Winter"
    elif 'Mar' in best_time or 'Apr' in best_time or 'May' in best_time:
        return "Spring"
    elif 'Jun' in best_time or 'Jul' in best_time or 'Aug' in best_time:
        return "Summer"
    else:
        return "Autumn"

df['peak_season'] = df['best_time'].apply(get_season)

season_counts = df['peak_season'].value_counts()
print("\n📅 Peak Season Distribution:")
for season, count in season_counts.items():
    print(f"   {season}: {count} countries")

# ============================================
# 8. TEMPERATURE ANALYSIS
# ============================================

print("\n" + "=" * 60)
print("8. TEMPERATURE ANALYSIS")
print("=" * 60)

print(f"\n🌡️ Average Temperature by Continent:")
temp_by_continent = df.groupby('continent')['temperature_c'].mean().round(1)
for continent, temp in temp_by_continent.items():
    print(f"   {continent}: {temp}°C")

print(f"\n🔥 Hottest Countries:")
hottest = df.nlargest(5, 'temperature_c')[['country', 'continent', 'temperature_c']]
for _, row in hottest.iterrows():
    print(f"   {row['country']:20} | {row['continent']:10} | {row['temperature_c']}°C")

print(f"\n❄️ Coldest Countries:")
coldest = df.nsmallest(5, 'temperature_c')[['country', 'continent', 'temperature_c']]
for _, row in coldest.iterrows():
    print(f"   {row['country']:20} | {row['continent']:10} | {row['temperature_c']}°C")

# ============================================
# 9. CURRENCY DISTRIBUTION
# ============================================

print("\n" + "=" * 60)
print("9. CURRENCY ANALYSIS")
print("=" * 60)

currency_counts = df['currency_code'].value_counts().head(10)
print("\n💱 Top 10 Currencies Used:")
for currency, count in currency_counts.items():
    print(f"   {currency}: {count} countries")

# ============================================
# 10. CUSTOMER-FRIENDLY QUERIES
# ============================================

print("\n" + "=" * 60)
print("10. CUSTOMER-FRIENDLY QUERIES")
print("=" * 60)

# Function to filter by budget
def filter_by_budget(budget, days=7, people=2):
    df['calculated_cost'] = (
        df['flight_cost_inr'] +
        (df['hotel_per_day_inr'] * days) +
        (df['food_per_day_inr'] * days) +
        (df['local_transport_inr'] * days) +
        df['visa_fee_inr']
    ) * people
    
    affordable = df[df['calculated_cost'] <= budget].copy()
    affordable = affordable.sort_values('calculated_cost')
    return affordable

# Example queries
print("\n🎯 Example Query 1: Budget ₹1,00,000 for 7 days, 2 people")
budget_1lakh = filter_by_budget(100000, 7, 2)
print(f"   Found {len(budget_1lakh)} countries")
for _, row in budget_1lakh.head(5).iterrows():
    print(f"   • {row['country']:20} | ₹{row['calculated_cost']:,.0f} | Safety: {row['safety_rating']}/10")

print("\n🎯 Example Query 2: Budget ₹2,00,000 for 10 days, 2 people")
budget_2lakh = filter_by_budget(200000, 10, 2)
print(f"   Found {len(budget_2lakh)} countries")
for _, row in budget_2lakh.head(5).iterrows():
    print(f"   • {row['country']:20} | ₹{row['calculated_cost']:,.0f} | Safety: {row['safety_rating']}/10")

print("\n🎯 Example Query 3: Only Asian countries with safety > 7")
asian_safe = df[(df['continent'] == 'Asia') & (df['safety_rating'] >= 7)]
asian_safe = asian_safe.sort_values('safety_rating', ascending=False)
print(f"   Found {len(asian_safe)} countries")
for _, row in asian_safe.head(5).iterrows():
    print(f"   • {row['country']:20} | Safety: {row['safety_rating']}/10 | Best: {row['best_time']}")

print("\n🎯 Example Query 4: Best winter destinations (Nov-Feb)")
winter_destinations = df[df['best_time'].str.contains('Nov|Dec|Jan|Feb', na=False)]
print(f"   Found {len(winter_destinations)} countries")
for _, row in winter_destinations.head(5).iterrows():
    print(f"   • {row['country']:20} | Best: {row['best_time']} | Temp: {row['temperature_c']}°C")

# ============================================
# 11. VISUALIZATION (If matplotlib installed)
# ============================================

print("\n" + "=" * 60)
print("11. VISUALIZATION (Saving charts...)")
print("=" * 60)

try:
    # Create figures directory
    os.makedirs('figures', exist_ok=True)
    
    # Figure 1: Countries by Continent
    plt.figure(figsize=(10, 6))
    continent_counts.plot(kind='bar', color=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe'])
    plt.title('Number of Countries by Continent', fontsize=14)
    plt.xlabel('Continent')
    plt.ylabel('Number of Countries')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('figures/continent_distribution.png')
    print("✅ Saved: figures/continent_distribution.png")
    
    # Figure 2: Safety Rating Distribution
    plt.figure(figsize=(10, 6))
    safety_counts.sort_index().plot(kind='bar', color='#667eea')
    plt.title('Safety Rating Distribution', fontsize=14)
    plt.xlabel('Safety Rating (1-10)')
    plt.ylabel('Number of Countries')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('figures/safety_distribution.png')
    print("✅ Saved: figures/safety_distribution.png")
    
    # Figure 3: Average Cost by Continent
    plt.figure(figsize=(10, 6))
    costs = df.groupby('continent')['total_cost_7days_2p'].mean().sort_values()
    costs.plot(kind='barh', color='#764ba2')
    plt.title('Average Trip Cost by Continent (7 days, 2 people)', fontsize=14)
    plt.xlabel('Average Cost (₹)')
    plt.tight_layout()
    plt.savefig('figures/cost_by_continent.png')
    print("✅ Saved: figures/cost_by_continent.png")
    
    # Figure 4: Budget Categories Pie Chart
    plt.figure(figsize=(8, 8))
    category_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#4caf50', '#ff9800', '#f44336', '#9c27b0'])
    plt.title('Countries by Budget Category', fontsize=14)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('figures/budget_categories.png')
    print("✅ Saved: figures/budget_categories.png")
    
    # Figure 5: Temperature Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df['temperature_c'].dropna(), bins=15, color='#ff9800', edgecolor='black')
    plt.title('Temperature Distribution Across Countries', fontsize=14)
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Number of Countries')
    plt.tight_layout()
    plt.savefig('figures/temperature_distribution.png')
    print("✅ Saved: figures/temperature_distribution.png")
    
except Exception as e:
    print(f"⚠️ Visualization error: {e}")
    print("   (Make sure matplotlib is installed: pip install matplotlib seaborn)")

# ============================================
# 12. SUMMARY REPORT
# ============================================

print("\n" + "=" * 60)
print("12. SUMMARY REPORT")
print("=" * 60)

print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    TRAVEL DATASET SUMMARY                     ║
╠══════════════════════════════════════════════════════════════╣
║  Total Countries:        {len(df):>45} ║
║  Continents:             {len(df['continent'].unique()):>45} ║
║  Avg Flight Cost:        ₹{df['flight_cost_inr'].mean():>10,.0f}                                   ║
║  Avg Hotel Cost:         ₹{df['hotel_per_day_inr'].mean():>10,.0f}/day                            ║
║  Avg Food Cost:          ₹{df['food_per_day_inr'].mean():>10,.0f}/day                            ║
║  Avg Safety Rating:      {df['safety_rating'].mean():>10.1f}/10                                 ║
║  Avg Temperature:        {df['temperature_c'].mean():>10.1f}°C                                  ║
╠══════════════════════════════════════════════════════════════╣
║  Cheapest Country:       {cheapest.iloc[0]['country']:>30} (₹{cheapest.iloc[0]['total_cost_7days_2p']:,.0f}) ║
║  Most Expensive:         {expensive.iloc[0]['country']:>30} (₹{expensive.iloc[0]['total_cost_7days_2p']:,.0f}) ║
║  Safest Country:         {safest.iloc[0]['country']:>30} ({safest.iloc[0]['safety_rating']}/10) ║
║  Best for Budget:        {cheapest.head(3)['country'].tolist()[0]}, {cheapest.head(3)['country'].tolist()[1]}, {cheapest.head(3)['country'].tolist()[2]} ║
╚══════════════════════════════════════════════════════════════╝
""")

# ============================================
# 13. EXPORT ANALYSIS
# ============================================

print("\n" + "=" * 60)
print("13. EXPORTING ANALYSIS RESULTS")
print("=" * 60)

# Save analysis results to CSV
df_with_cost = filter_by_budget(500000, 7, 2)  # Temporary for calculation
analysis_results = df[['country', 'continent', 'flight_cost_inr', 'hotel_per_day_inr', 
                        'food_per_day_inr', 'safety_rating', 'temperature_c', 'currency_code']].copy()
analysis_results.to_csv('data_analysis_output.csv', index=False)
print("✅ Saved: data_analysis_output.csv")

# Save budget categories
category_summary = df.groupby('budget_category').size().reset_index(name='count')
category_summary.to_csv('budget_categories_summary.csv', index=False)
print("✅ Saved: budget_categories_summary.csv")

print("\n" + "=" * 60)
print("✅ ANALYSIS COMPLETE!")
print("=" * 60)

# Optional: Interactive query function
def interactive_query():
    print("\n" + "=" * 60)
    print("INTERACTIVE QUERY MODE")
    print("=" * 60)
    
    while True:
        print("\nOptions:")
        print("1. Filter by budget")
        print("2. Filter by continent")
        print("3. Filter by safety rating")
        print("4. Filter by temperature")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ")
        
        if choice == '1':
            budget = float(input("Enter your budget (₹): "))
            days = int(input("Number of days: "))
            people = int(input("Number of people: "))
            result = filter_by_budget(budget, days, people)
            print(f"\n✅ Found {len(result)} countries within ₹{budget:,.0f}")
            print(result[['country', 'continent', 'calculated_cost', 'safety_rating']].head(10).to_string(index=False))
        
        elif choice == '2':
            continent = input("Enter continent (Asia/Europe/Africa/Americas/Oceania): ")
            result = df[df['continent'] == continent]
            print(f"\n✅ Found {len(result)} countries in {continent}")
            print(result[['country', 'safety_rating', 'temperature_c']].head(10).to_string(index=False))
        
        elif choice == '3':
            min_safety = float(input("Minimum safety rating (1-10): "))
            result = df[df['safety_rating'] >= min_safety]
            print(f"\n✅ Found {len(result)} countries with safety ≥ {min_safety}")
            print(result[['country', 'continent', 'safety_rating']].sort_values('safety_rating', ascending=False).head(10).to_string(index=False))
        
        elif choice == '4':
            min_temp = float(input("Minimum temperature (°C): "))
            max_temp = float(input("Maximum temperature (°C): "))
            result = df[(df['temperature_c'] >= min_temp) & (df['temperature_c'] <= max_temp)]
            print(f"\n✅ Found {len(result)} countries between {min_temp}°C and {max_temp}°C")
            print(result[['country', 'continent', 'temperature_c']].head(10).to_string(index=False))
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice!")

# Uncomment to run interactive query
# interactive_query()