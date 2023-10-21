# must run source .venv/bin/activate before running app.py

from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

token = os.environ.get("password")
# print(token)

uri = "mongodb+srv://lnb337:" + token + "@cluster0-stuy.5kw8pxw.mongodb.net/?retryWrites=true&w=majority"

# print(token)



# Create a new client and connect to the server
client = MongoClient(uri)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['project2-database']
collection = db['sales']
print(collection.find_one())

travels = db['travel-plans']
travels.insert_one({'plan_name':'Trip to Ibiza', 'dates':'10-19-23 -- 10-27-23', 'travel_method':'plane', 'notes':'bring sunscreen'})
print(travels.find_one())
print('pls')