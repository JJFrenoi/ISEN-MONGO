from pymongo import MongoClient

print('Lille exemple coords : Latitude : 50.6329700 / Longitude : 3.0585800')
print('Lyon exemple coords : Latitude : 45.755539 / Longitude : 4.797010\n')

atlas = MongoClient("mongodb+srv://root:root@cluster0.8wh7w.mongodb.net/bicycle?retryWrites=true&w=majority")

db = atlas.bicycle
stations = db.stations
lille = db.datas

print("Les villes supportées sont Lille, Lyon, Paris et Rennes. Cependant, seul Lille possède les données en temps réel\n")

lat = float(input("Entrez la latitude : "))
lon = float(input("Entrez la longitude : "))

recherche = {'geometry': {'$near': {'$geometry': {'type': "Point", 'coordinates': [lon, lat]}, '$minDistance': 0, '$maxDistance': 500}}}
# Autre possibilité plus rapide mais les données ne sont plus triées de la plus proche à la plus éloignée
# recherche = { 'geometry': { '$geoWithin': { '$centerSphere' : [[lon, lat], 500/6378100] } } }

results = stations.find(recherche)

# Le count est déprécié mais son alternative count_documents ne fonctionne pas avec $near...
if results.count() != 0:
    print('\nLes stations suivantes sont disponibles dans un rayon de 500m :\n')
    for res in results:
        if 50.0 < lat < 51.0 and 2.5 < lon < 3.5:
            data = lille.find({'station_id': res['_id']})
            if data.count() > 0:
                data = data.next()
                print(res['name'] + ' [nb vélos dispo : ' + str(data['bike_available']) +
                  '] / [nb places libres : ' + str(data['stand_available']) + ']')
            else:
                print(res['name'])
        else:
            print(res['name'])
else:
    print('Aucune station n\'est disponible dans un rayon de 500m')
