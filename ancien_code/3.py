import requests
import json
from pprint import pprint
from pymongo import MongoClient


# Lille exemple coords
# Latitude : 50.6329700°
# Longitude : 3.0585800° 

if __name__ == "__main__":
	client = MongoClient("mongodb+srv://jeanBis:123jean@cluster0.leyqh.gcp.mongodb.net/BicycleStations?retryWrites=true&w=majority")
	db = client.BicycleStations
	bicycle_station = db['bicycle_station']
	lille = db['Lille']

	print("Les villes supportées sont Lille, Lyon, Paris et Rennes")

	lat = float(input("Entrez la latitude : "))
	lon = float(input("Entrez la longitude : "))

	results = bicycle_station.find({
		'geolocations':
			{ '$near':
				{
					'$geometry': { 'type': "Point",  'coordinates': [  lon, lat ] },
					'$minDistance': 0,
					'$maxDistance': 500
				}
			}
		})
	
	if results.count() != 0 :
		print('Les stations suivantes sont disponibles dans un rayon de 500m :')
		for res in results:
			t = lille.find({
				'name': res['name']
				})
			print(res['name'] + '(' + str(t.next()['size']) + ')')
	else:
		print('Aucune station n\'est disponible dans un rayon de 500m')
