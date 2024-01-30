from json_reader.city import CityCollection


class AutocompleteHelper:
    map = {}

    def load_from(self, cities_collection: CityCollection):
        self.map = {}
        cities = cities_collection.get_all()
        for city in cities:
            try:
                key = city.name + ", " + city.state
                self.map[key] = city
            except TypeError:
                print("No state definition for " + city.name)

    def find_by_key(self, key: str):
        return self.map[key]

    def all_keys(self):
        return list(self.map.keys())
