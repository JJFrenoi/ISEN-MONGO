from Bdd import Bdd
if __name__ == "__main__":
    push = Bdd()

    lilleurl = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    rennes_temps_reel = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
    reenes_statique = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=stations_vls&q="

    lyon_temps_reel = "https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json?maxfeatures=100&start=1"
    lyon_statique = "https://download.data.grandlyon.com/ws/grandlyon/pvo_patrimoine_voirie.pvostationvelov/all.json?maxfeatures=100&start=1"

    paris_temps_reel = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"
    paris_statique = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-emplacement-des-stations&q="

    id = push.push(lilleurl ,'Lille')
    print('id: ', id[0])
    id1 = push.push(lyon_statique , 'Lyon')
    print ('id1', id1[0])
    id2 = push.push(paris_statique,'Paris')
    print('id2', id2[0])
    id3 = push.push(reenes_statique, 'Rennes')
    print('id3',id3[0])

    historyWorker = push.refreshAndPush(paris_temps_reel, 'Paris')
