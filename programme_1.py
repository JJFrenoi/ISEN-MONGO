import requests
import json
from pprint import pprint
from pymongo import MongoClient


def get_vlille():
	url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"

	response = requests.request("GET", url, headers={}, data = {})
	response_json = json.loads(response.text.encode('utf8'))
	return response_json.get("records", [])


def get_vrennes():
	#url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
	url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=stations_vls&q=&rows=3000"

	response = requests.request("GET", url, headers={}, data = {})
	response_json = json.loads(response.text.encode('utf8'))
	return response_json.get("records", [])


def get_vlyon():
	#url = "https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json?maxfeatures=100&start=1"
	url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=station-velov-grand-lyon&q=&facet=name&facet=status&rows=500"

	response = requests.request("GET", url, headers={}, data = {})
	response_json = json.loads(response.text.encode('utf8'))
	return response_json.get("records", [])


def get_vparis():
	url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&facet=name&facet=is_renting&rows=300"
	#url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-emplacement-des-stations&q="

	response = requests.request("GET", url, headers={}, data = {})
	response_json = json.loads(response.text.encode('utf8'))
	return response_json.get("records", [])


vlilles = get_vlille()
vrennes = get_vrennes()
vlyon = get_vlyon()
vparis = get_vparis()

vlliles_to_insert = [
	{
		'name': elem.get('fields', {}).get('nom', ''),
		'geometry': elem.get('geometry'),
		'size': elem.get('fields', {}).get('nbvelosdispo') + elem.get('fields', {}).get('nbplacesdispo'),
		'source': {
			'dataset': 'Lille',
			'id_ext': elem.get('fields', {}).get('libelle')
		},
		'tpe': elem.get('fields', {}).get('type', '') == 'AVEC TPE',
		'available': elem.get('fields', {}).get('etat', '') == 'EN SERVICE'
	}
	for elem in vlilles
]

vrennes_to_insert = [
	{
		'name': elem.get('fields', {}).get('nom', ''),
		'geometry': elem.get('geometry'),
		'size': elem.get('fields', {}).get('nb_socles'),
		'source': {
			'dataset': 'Rennes',
			'id_ext': elem.get('fields', {}).get('objectid')
		},
		'tpe': elem.get('fields', {}).get('tpe', '') == 'oui',
		'available': elem.get('fields', {}).get('etat', '') == 'Ouverte'
	}
	for elem in vrennes
]

vlyon_to_insert = [
	{
		'name': elem.get('fields', {}).get('name', ''),
		'geometry': elem.get('geometry'),
		'size': elem.get('fields', {}).get('bike_stand'),
		'source': {
			'dataset': 'Lyon',
			'id_ext': int(elem.get('fields', {}).get('gid'))
		},
		'tpe': elem.get('fields', {}).get('banking', '') == 't',
		'available': elem.get('fields', {}).get('status', '') == 'OPEN'
	}
	for elem in vlyon
]

vparis_to_insert = [
	{
		'name': elem.get('fields', {}).get('name', ''),
		'geometry': elem.get('geometry'),
		'size': elem.get('fields', {}).get('capacity'),
		'source': {
			'dataset': 'Paris',
			'id_ext': int(elem.get('fields', {}).get('stationcode'))
		},
		'tpe': False,
		'available': elem.get('fields', {}).get('is_renting', '') == 'OUI'
	}
	for elem in vparis
]

pprint(vlliles_to_insert)
pprint(vrennes_to_insert)
pprint(vlyon_to_insert)
pprint(vparis_to_insert)

atlas = MongoClient('mongodb+srv://root:root@cluster0.8wh7w.mongodb.net/bicycle?retryWrites=true&w=majority')

db = atlas.bicycle
db.stations.create_index([("geometry", "2dsphere")])
db.stations.insert_many(vlliles_to_insert)
db.stations.insert_many(vrennes_to_insert)
db.stations.insert_many(vlyon_to_insert)
db.stations.insert_many(vparis_to_insert)

#for vlille in vlliles_to_insert:
#	db.stations.insert_one(vlille)