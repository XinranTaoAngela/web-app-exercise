
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://lnb337:8nWKMQ2CbVFLHEMl@cluster0-stuy.5kw8pxw.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['sample_supplies']
collection = db['sales']
print(collection.find_one())