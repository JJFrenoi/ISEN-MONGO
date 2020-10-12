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
            if ville == 'Lille' or ville == 'Rennes' or ville == 'Paris' or ville == 'Lyon':
                records = response_json.get('records')
                collection = self.db['bicycle_station']
                collectionVille = self.db[ville]
                if ville in self.collectionList:
                    collectionVille.drop()
                result = []
                for record in records:
                    fields = record.get('fields')
                    #print(fields)
                    if (ville == 'Lille'):
                        object = {
                            'geolocations': record.get('geometry'),
                            'size': fields.get('nbvelosdispo')+fields.get('nbplacesdispo'),
                            'name': fields.get('nom'),
                            'tpe': True if (fields.get('type') == 'AVEC TPE') else False,
                            'available': True if (fields.get('etat') == 'EN SERVICE') else False
                        }
                    elif (ville == 'Rennes'):
                        object = {
                            'geolocations': record.get('geometry'),
                            'size': fields.get('nb_socles'),
                            'name': fields.get('nom'),
                            'tpe': True if (fields.get('tpe') == 'oui') else False,
                            'available': True if (fields.get('etat') == 'Ouverte') else False
                        }
                    elif (ville == 'Paris'):
                        object = {
                            'geolocations': record.get('geometry'),
                            'size': fields.get('capacity'),
                            'name': fields.get('name'),
                            'tpe': False,
                            'available': True if (fields.get('is_renting') == 'OUI') else False
                        }
                    elif (ville == 'Lyon'):
                        object = {
                            'geolocations': record.get('geometry'),
                            'size': fields.get('bike_stand'),
                            'name': fields.get('name'),
                            'tpe': True if (fields.get('banking') == 't') else False,
                            'available': True if (fields.get('status') == 'OPEN') else False
                        }
                    id = collection.insert_one(object)
                    collectionVille.insert_one(object)
                    result.append(id.inserted_id)

            else:
                return ["Ville not found"]
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
    
    def drop(self,collection):
        self.db[collection].drop()

    def push(self, dataUrl, ville):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            thread = executor.submit(
                lambda p: self.threadedPush(*p), [dataUrl, ville])
            return thread.result()
