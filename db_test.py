from pymongo import MongoClient
import datetime
client = MongoClient()
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['project2-database']
collection = db['travel-plans']
collection.delete_many({})
collection.insert_one({'plan_name':'Trip to Ibiza', 'dep_date':datetime.datetime.now(), 
                       'ret_date':datetime.datetime.now(), 'travel_method':'plane', 'notes':'bring sunscreen'})
for post in collection.find():
    print(post)
# print(collection.find_one())