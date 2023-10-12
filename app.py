# must run source .venv/bin/activate before running app.py

from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

token = os.environ.get("password")
# print(token)

uri = "mongodb+srv://lnb337:" + token + "@cluster0-stuy.5kw8pxw.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['sample_supplies']

travels = db['travels']
travels.insert_one({'name': 'Lily', 'country': 'USA', 'itinerary': ['NYC', 'LA', 'SF']})
print(travels.find_one())
print('pls')