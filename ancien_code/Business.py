from Bdd import Bdd
class Business(Bdd):
    def findByName(self,name):
        collection = self.db['bicycle_station']
        liste = collection.find({"name": {"$regex": name}})
        for station in liste:
            print(station)

    def deletebyName(self, name):
        collection = self.db['bicycle_station']
        collection.delete_many(
            {"name": {"$regex": name}})

    def update(self, parameter_list):
        """
        docstring
        """
        pass
