from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from collections import Counter

app = Flask(__name__)

# recommendations = [
#     {"name": "Giza August Trip", "dates": "August 27-29, 2024", "travel_method": "Flight"},
#     {"name": "Mars 3-Day Trip", "dates": "Future Date", "travel_method": "Spacecraft"},
# ]

recommendations = [
    {
        "plan_name": "Trip to Paris",
        "dep_date": "2023-05-15",
        "ret_date": "2023-05-25",
        "travel_method": "Flight",
        "notes": "Visiting the Eiffel Tower."
    },
    {
        "plan_name": "Beach Vacation",
        "dep_date": "2023-07-10",
        "ret_date": "2023-07-20",
        "travel_method": "Car",
        "notes": "Relaxing by the seaside."
    },
    {
        "plan_name": "Ski Trip",
        "dep_date": "2023-12-20",
        "ret_date": "2023-12-30",
        "travel_method": "Bus",
        "notes": "Enjoying the snowy slopes."
    },
    {
        "plan_name": "Business Conference",
        "dep_date": "2023-09-05",
        "ret_date": "2023-09-10",
        "travel_method": "Train",
        "notes": "Attending industry meetings."
    },
    {
        "plan_name": "Road Trip",
        "dep_date": "2023-06-25",
        "ret_date": "2023-07-05",
        "travel_method": "RV",
        "notes": "Exploring national parks."
    }
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



@app.route('/', methods=['GET', 'POST'])
def home():
    all_plans = []
    for post in collection.find():
        all_plans.append(post) # test
    query = None
    if request.method == 'POST':
        query = request.form.get('search_query').lower()
        filtered_plans = [plan for plan in all_plans if query in plan['plan_name'].lower()]
        return render_template('home.html', plans=filtered_plans)
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
    all_plans = []
    for post in collection.find():
        all_plans.append(post) # test

    if request.method == 'POST':
        edit_plan = request.form.get("plan_to_edit")
        plan_name = request.form.get("plan_name")
        dep_date = request.form.get("dep_date")
        ret_date = request.form.get("ret_date")
        travel_method = request.form.get("travel_method")
        notes = request.form.get("notes")

        doc_to_edit = collection.find_one({"plan_name": edit_plan})
        if dep_date == "":
            dep_date = doc_to_edit["dep_date"]
        if ret_date == "":
            ret_date = doc_to_edit["ret_date"]
        if travel_method == "":
            travel_method = doc_to_edit["travel_method"]
        if notes == "":
            notes = doc_to_edit["notes"]
        

        doc = {
            "plan_name": plan_name, 
            "dep_date": dep_date,
            "ret_date": ret_date,
            "travel_method": travel_method,
            "notes": notes,
        }

        print(doc)

        collection.update_one({"plan_name": edit_plan}, {"$set": doc})

        return redirect(url_for('home'))
    
    return render_template('edit_plan.html', plans=all_plans)

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
    travel_methods = [plan['travel_method'] for plan in all_plans]
    most_common = Counter(travel_methods).most_common(1)[0][0] if travel_methods else "N/A"
    
    if request.method == 'POST':
        collection.find_one_and_delete({"plan_name": request.form.get("plan_name")})
    return render_template('user_info.html', most_frequent_travel=most_common, plans=all_plans)
    

@app.route('/delete-plan', methods=['POST'])
def delete_plan():
    if request.method == 'POST':
        plan_name = request.form.get('plan_to_delete')
        print('temp',plan_name)
        collection.find_one_and_delete({"plan_name": plan_name})
    
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
