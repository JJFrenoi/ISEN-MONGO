import json
import re
from pprint import pprint
from pymongo import MongoClient

atlas = MongoClient("mongodb+srv://root:root@cluster0.8wh7w.mongodb.net/bicycle?retryWrites=true&w=majority")

db = atlas.bicycle
stations = db.stations
lille = db.datas


def rechercher_station(nom):
    regex_nom = re.compile(nom, re.IGNORECASE)

    recherche = {"name": regex_nom}
    nb_resultats = stations.count_documents(recherche)
    resultats = stations.find(recherche)

    if nb_resultats == 0:
        return 0
    else:
        return [nb_resultats, resultats]


def moditifer_station(id, champ, valeur):
    stations.update_one({"_id": id}, {"$set": {champ: valeur}})


def supprimer_station(id, nom_ville):
    stations.delete_one({"_id": id})

    if nom_ville == "Lille":
        lille.delete_many({"station_id": id})


def gestion_zone(status):
    liste_stations = []

    with open("zone.geojson", 'r') as geojson:
        geojson = geojson.read()
        donnees_json = json.loads(geojson)

        recherche = {"geometry": {"$geoWithin": {"$geometry": donnees_json["features"][0]["geometry"]}}}
        resultats = stations.find(recherche)
        for resultat in resultats:
            liste_stations.append(resultat['name'])

        stations.update_many(recherche, {"$set": {"available": status}})
    return liste_stations


try:
    choix = input("Voulez-vous effectuer une recherche de station [R] ou manipuler une zone [Z] : ")
    while choix != 'R' and choix != 'r' and choix != 'Z' and choix != 'z':
        choix = input("Voulez-vous effectuer une recherche de station [R] ou manipuler une zone [Z] : ")

    # Recherche de stations
    if choix == 'R' or choix == 'r':
        nom = input("Entrez votre recherche : ")
        resultats_recherche = rechercher_station(nom)
        # On boucle tant qu'on n'a pas trouvé au moins une station
        while resultats_recherche == 0:
            nom = input("Pas de résultat, essayez une nouvelle recherche : ")
            resultats_recherche = rechercher_station(nom)

        print("\n%d station(s) ont été trouvée(s)\n" % resultats_recherche[0])
        liste = list(resultats_recherche[1])
        for elem in liste:
            pprint(elem)
            print('\n')

        choix = int(
            input("Sélectionnez l'index (débutant à 0) de la station que vous souhaitez modifier ou supprimer : "))
        elem_choisi = liste[choix]
        choix = input("Voulez-vous modifier [M] ou supprimer [S] la station : ")
        # Choix entre la modification ou la suppression d'une station
        while choix != 'M' and choix != 'm' and choix != 'S' and choix != 's':
            choix = input("Voulez-vous modifier [M] ou supprimer [S] la station : ")

        # Cas de la modification d'une station
        if choix == 'M' or choix == 'm':
            print("\nEdition de la station : " + elem_choisi["name"])
            choix = input("Voulez-vous modifier le champ name [N] ou le champ size [S] : ")
            while choix != 'N' and choix != 'n' and choix != 'S' and choix != 's':
                choix = input("Voulez-vous modifier le champ 'name' [N] ou le champ 'size' [S] : ")

            if choix == 'N' or choix == 'n':
                nouveau_nom = input("Choississez le nouveau nom : ")
                moditifer_station(elem_choisi["_id"], "name", nouveau_nom)
                print("\nLa station " + elem_choisi["name"] + " a désormais le nom " + nouveau_nom)
            elif choix == 'S' or choix == 's':
                nouvelle_taille = int(input("Choississez la nouvelle taille : "))
                moditifer_station(elem_choisi["_id"], "size", nouvelle_taille)
                print("\nLa station " + elem_choisi["name"] + " accueille désormais " + str(nouvelle_taille) + " vélos")

        # Cas de la suppression d'une station (et ses données si elle se trouve à Lille)
        elif choix == 'S' or choix == 's':
            supprimer_station(elem_choisi["_id"], elem_choisi["source"]["dataset"])
            print("\nLa station " + elem_choisi["name"] + " a bien été supprimée")

    # Activation/Désactivation des stations dans une zone délimitée par un geojson
    elif choix == 'Z' or choix == 'z':
        choix = input('Voulez-vous activer [A] ou désactiver [D] les stations dans la zone : ')
        while choix != 'A' and choix != 'a' and choix != 'D' and choix != 'd':
            choix = input('Voulez-vous activer [A] ou désactiver [D] les stations dans la zone : ')

        if choix == 'A' or choix == 'a':
            status = True
            status_texte = "activées"
        elif choix == 'D' or choix == 'd':
            status = False
            status_texte = "désactivées"

        stations_changees = gestion_zone(status)
        print("\n Les stations suivantes ont été " + status_texte + " : ")
        print(stations_changees)

    print('\n- Fin du programme -')
except Exception as e:
    print('\nChoix impossible ou une erreur a eu lieu. Arrêt du programme !\n')
    pprint(e)
