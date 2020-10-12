import requests
from pymongo import MongoClient
import json
import concurrent.futures
import time
import threading


class Bdd:

    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://jeanBis:123jean@cluster0.leyqh.gcp.mongodb.net/BicycleStations?retryWrites=true&w=majority")
        self.db = self.client.BicycleStations
        self.collectionList = self.db.list_collection_names()
        for col in self.collectionList:
            print(col)

    def userPrograme(self, lat, lon, ville):
        pass

    def threadedRefresh(self, dataUrl, ville):
        while True:
            try:
                print("Starting")
                response = requests.request(
                    "GET", dataUrl, headers={}, data={})
                response_json = json.loads(response.text.encode('utf8'))
                if ville == 'Lille' or ville == 'Rennes' or ville == 'Paris':
                    records = response_json.get('records')
                elif ville == 'Lyon':
                    records = response_json.get('values')
                else:
                    print('Ville not found')
                collection = self.db[ville + 'history']
                collection.insert_many(records)
            except Exception as identifier:
                print(identifier)
            except (KeyboardInterrupt, SystemExit):
                print(KeyboardInterrupt)
                raise
            finally:
                time.sleep(60.0)

    def threadedPush(self, dataUrl, ville):
        try:
            response = requests.request(
                "GET", dataUrl, headers={}, data={})
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
            result = []
            for record in records:
                fields = record.get('fields')
                print(fields)
                object = {
                    'geolocations': fields.get('localisation'),
                    'size': fields.get('nbvelosdispo')+fields.get('nbplacesdispo'),
                    'name': fields.get('nom'),
                    'tpe': fields.get('type'),
                    'available': fields.get('etat')
                }
                id = collection.insert_one(object)
                result.append(id.inserted_id)

            #result = collection.insert_many(records)
        except Exception as identifier:
            print(identifier)
            return ["failed"]
        finally:
            # return result.inserted_ids
            return result

    def refreshAndPush(self, dataUrl, ville):
        refreshThread = threading.Thread(
            target=self.threadedRefresh, args=(dataUrl, ville,))
        refreshThread.start()

    def push(self, dataUrl, ville):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            thread = executor.submit(
                lambda p: self.threadedPush(*p), [dataUrl, ville])
            return thread.result()
