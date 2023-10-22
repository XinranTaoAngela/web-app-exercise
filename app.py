from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

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

# Connect to MongoDB
client = MongoClient()
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['project2-database']
collection = db['travel-plans']

# get all documents from the collection
all_plans = []
for post in collection.find():
    all_plans.append(post) # test

# print('does',all_plans)


@app.route('/')
def home():
    all_plans = []
    for post in collection.find():
        all_plans.append(post) # test

    if request.method == 'POST':
        collection.find_one({"plan_name": request.form.get("plan_name")})

    return render_template('home.html', plans=all_plans)

@app.route('/create-plan', methods=['GET', 'POST'])
def create_plan():
    if request.method == 'POST':
        # Capture form data and add to plans list (for simplicity)
        collection.insert_one({"plan_name": request.form.get("plan_name"),
        "dep_date": request.form.get("dep_date"),
        "ret_date": request.form.get("ret_date"),
        "travel_method": request.form.get("travel_method"),
        "notes": request.form.get("notes")})
        
        return redirect(url_for('home'))
    return render_template('create_plan.html')

@app.route('/edit-plan', methods=['GET', 'POST'])
def edit_plan():
    # plan = plans[plan_id]
    # if request.method == 'POST':
    #     # Update plan details
    #     plan["name"] = request.form.get("plan_name")
    #     plan["dates"] = request.form.get("dates")
    #     plan["travel_method"] = request.form.get("travel_method")
    #     plan["notes"] = request.form.get("notes")
    #     return redirect(url_for('home'))
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
    # Implementation for displaying user info
    if request.method == 'POST':
        collection.find_one_and_delete({"plan_name": request.form.get("plan_name")})
    return render_template('user_info.html')

if __name__ == "__main__":
    app.run(debug=True)
