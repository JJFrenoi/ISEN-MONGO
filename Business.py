from Bdd import Bdd
class Business(Bdd):
    def findByName(self,name):
        collection = self.db['bicycle_station']
        list_stations = collection.find({"name": {"$regex": name}})
        for station in list_stations:
            print(station)


    def update(self, parameter_list):
        """
        docstring
        """
        pass
