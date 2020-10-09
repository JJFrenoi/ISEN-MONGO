from PushApitoBdd import PushApitoBdd
if __name__ == "__main__":
    push = PushApitoBdd()
    id = push.push("https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion",
                   'Lille')
    print('id: ',id)
