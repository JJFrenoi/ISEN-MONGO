import requests
from pymongo import MongoClient
import json


class PushApitoBdd:

    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://jeanBis:123jean@cluster0.leyqh.gcp.mongodb.net/BicycleStations?retryWrites=true&w=majority")
        self.db = self.client.BicycleStations
        self.collectionList = self.db.list_collection_names()
        for col in self.collectionList:
            print(col)

    def push(self, dataUrl, ville):
        payload = {}
        headers = {}
        try:
            response = requests.request(
                "GET", dataUrl, headers=headers, data=payload)
            response_json = json.loads(response.text.encode('utf8'))
            if ville == 'Lille' or ville == 'Rennes' or ville == 'Paris':
                records = response_json.get('records')
            elif ville == 'Lyon':
                records = response_json.get('values')
            else:
                return ["Ville not found"]
            collection = self.db[ville]
            if ville in self.collectionList:
                collection.drop()
            result = collection.insert_many(records)
        except Exception as identifier:
            print(identifier)
            return ["failed"]
        finally:
            return result.inserted_ids
