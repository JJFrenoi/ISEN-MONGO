from Bdd import Bdd
from Business import Business
import concurrent.futures

if __name__ == "__main__":
    push = Bdd()
    business = Business()

    lilleurl = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    rennes_temps_reel = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
    rennes_statique = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=stations_vls&q=&rows=3000"

    lyon_temps_reel = "https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json?maxfeatures=100&start=1"
    lyon_statique = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=station-velov-grand-lyon&q=&facet=name&facet=status&rows=500"

    paris_temps_reel = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&facet=name&facet=is_renting&rows=300"
    paris_statique = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-emplacement-des-stations&q="
    #push.drop('bicycle_station')
    #id = push.push(lilleurl, 'Lille')
    #print('id: ', id[0])
    #id1 = push.push(lyon_statique, 'Lyon')
    #print('id1', id1[0])
    #id2 = push.push(paris_temps_reel, 'Paris')
    #print('id2', id2[0])
    #id3 = push.push(rennes_statique, 'Rennes')
    #print('id3', id3[0])
    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #     thread0 = executor.submit(
    #         lambda p: push.threadedPush(*p), [lilleurl, 'Lille'])
    #     thread1 = executor.submit(
    #         lambda p: push.threadedPush(*p), [lyon_statique, 'Lyon'])
    #     thread2 = executor.submit(
    #         lambda p: push.threadedPush(*p), [paris_temps_reel, 'Paris'])
    #     thread3 = executor.submit(
    #         lambda p: push.threadedPush(*p), [rennes_statique, 'Rennes'])
    #     print('id0:', thread0.result()[0])
    #     print('id1:', thread1.result()[0])
    #     print('id2:', thread2.result()[0])
    #     print('id3:', thread3.result()[0])

    #push.refreshAndPush(paris_temps_reel, 'Paris')
    #push.userPrograme(50.63393, 3.061687, 'Lille', 400)
    business.findByName("HOPITAL")
    business.deletebyName("HOPITAL")
    business.findByName("HOPITAL")
