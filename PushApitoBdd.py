import requests
from pymongo import MongoClient
import json


class PushApitoBdd:

    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://jeanBis:123jean@cluster0.leyqh.gcp.mongodb.net/BicycleStations?retryWrites=true&w=majority")
        self.db = self.client.BicycleStations

    def push(self, dataUrl, ville):
        payload = {}
        headers = {}
        response = requests.request(
            "GET", dataUrl, headers=headers, data=payload)
        response_json = json.loads(response.text.encode('utf8'))
        if ville == 'Lille':
                collection = self.db.Lille
                result = collection.insert_one(response_json)
                return result.inserted_id
        return 'failed'
