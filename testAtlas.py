from pymongo import MongoClient
from pprint import pprint 

client = MongoClient(
    "mongodb+srv://jeanBis:123jean@cluster0.leyqh.gcp.mongodb.net/ISEN?retryWrites=true&w=majority")
db = client.ISEN
collection = db.dbisen
result = collection.insert_one({
    "name": "Tyrion",
    "age": 25
})

print('_id:', result.inserted_id)

collection.insert_one({
    "name": "Daenerys",
    "age": 17
})


# read data
cursors = collection.find({})
for element in cursors:
    pprint(element)

# or get all data response in ram
cursors = collection.find({})
my_result = list(cursors)
pprint(my_result)
