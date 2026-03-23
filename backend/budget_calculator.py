# ============================================
# Travel Budget Calculator - FINAL VERSION
# Phase 0 - Python Basics Complete
# ============================================


# ---- FUNCTION 1: User se data lo ----
def get_user_input():
    print("=" * 45)
    print("      TRAVEL BUDGET CALCULATOR")
    print("=" * 45)
    name   = input("Aapka naam: ")
    budget = float(input("Travel budget (Rs mein): "))
    days   = int(input("Kitne din: "))
    people = int(input("Kitne log: "))
    return name, budget, days, people


# ---- FUNCTION 2: Calculate karo ----
def calculate_budget(budget, days, people):
    per_day    = budget / days
    per_person = budget / people
    return per_day, per_person


# ---- FUNCTION 3: Destination suggest karo ----
def suggest_destination(budget):
    if budget >= 200000:
        return "International — Europe/Japan/USA"
    elif budget >= 80000:
        return "International Asia — Thailand/Dubai/Nepal"
    elif budget >= 30000:
        return "Domestic Premium — Goa/Kashmir/Manali"
    else:
        return "Domestic Budget — Nearby states"


# ---- FUNCTION 4: Result dikhao ----
def show_result(name, budget, per_day, per_person, destination):
    print("\n" + "=" * 45)
    print(f"  Namaste {name}! Aapki detail:")
    print(f"  Total Budget  : Rs {budget:,.0f}")
    print(f"  Per Day       : Rs {per_day:,.0f}")
    print(f"  Per Person    : Rs {per_person:,.0f}")
    print(f"  Best Option   : {destination}")
    print("=" * 45)


# ---- FUNCTION 5: Dobara try karna ----
def run_app():
    while True:
        # Sab functions call karo
        name, budget, days, people = get_user_input()
        per_day, per_person        = calculate_budget(budget, days, people)
        destination                = suggest_destination(budget)
        show_result(name, budget, per_day, per_person, destination)

        # Dobara try karna hai?
        print()
        dobara = input("Dobara try karein? (haan/nahi): ").strip().lower()
        if dobara == "nahi":
            print("\nShukriya! Milte hain project mein. 👋")
            break


# ============================================
# PROGRAM START
# ============================================
run_app()
