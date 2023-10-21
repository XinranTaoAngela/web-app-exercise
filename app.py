from flask import Flask, render_template, request, redirect, url_for
from collections import Counter

app = Flask(__name__)

# Sample Data
plans = [
    {"name": "Rome Trip May 2023", "dates": "10/6 - 10/30", "travel_method": "Flight", "notes": ""},
    {"name": "NY Family Vacation Aug 2024", "dates": "8/12-8/17", "travel_method": "Plane", "notes": ""},
]

recommendations = [
    {"name": "Giza August Trip", "dates": "August 27-29, 2024", "travel_method": "Flight"},
    {"name": "Mars 3-Day Trip", "dates": "Future Date", "travel_method": "Spacecraft"},
]

@app.route('/', methods=['GET', 'POST'])
def home():
    query = None
    if request.method == 'POST':
        query = request.form.get('search_query').lower()
        filtered_plans = [plan for plan in plans if query in plan['name'].lower()]
        return render_template('home.html', plans=filtered_plans)
    return render_template('home.html', plans=plans)

@app.route('/create-plan', methods=['GET', 'POST'])
def create_plan():
    if request.method == 'POST':
        # Capture form data and add to plans list (for simplicity)
        plans.append({
            "name": request.form.get("plan_name"),
            "dates": request.form.get("dates"),
            "travel_method": request.form.get("travel_method"),
            "notes": request.form.get("notes"),
        })
        return redirect(url_for('home'))
    return render_template('create_plan.html')

@app.route('/edit-plan/<int:plan_id>', methods=['GET', 'POST'])
def edit_plan(plan_id):
    plan = plans[plan_id]
    if request.method == 'POST':
        # Update plan details
        plan["name"] = request.form.get("plan_name")
        plan["dates"] = request.form.get("dates")
        plan["travel_method"] = request.form.get("travel_method")
        plan["notes"] = request.form.get("notes")
        return redirect(url_for('home'))
    return render_template('edit_plan.html', plan=plan)

@app.route('/create-plan-days', methods=['GET', 'POST'])
def create_plan_days():
    # Implementation for creating plan days
    return render_template('create_plan_days.html')

@app.route('/edit-plan-days', methods=['GET', 'POST'])
def edit_plan_days():
    # Implementation for editing plan days
    return render_template('edit_plan_days.html')

@app.route('/recommendations')
def recommendations_page():
    return render_template('recommendations.html', recommendations=recommendations)

@app.route('/user-info')
def user_info():
    travel_methods = [plan['travel_method'] for plan in plans]
    most_common = Counter(travel_methods).most_common(1)[0][0] if travel_methods else "N/A"
    return render_template('user_info.html', most_frequent_travel=most_common, plans=plans)

@app.route('/delete-plan', methods=['POST'])
def delete_plan():
    plan_name = request.form.get('plan_to_delete')
    global plans
    plans = [plan for plan in plans if plan['name'] != plan_name]
    return redirect(url_for('user_info'))

if __name__ == "__main__":
    app.run(debug=True)
