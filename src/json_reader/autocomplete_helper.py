from json_reader.city import CityCollection, CityInfo


class AutocompleteHelper:
    map: dict[str, CityInfo] = {}

    def load_from(self, cities_collection: CityCollection):
        self.map = {}
        cities = cities_collection.get_all()
        cities = sorted(cities, key=lambda city: city.population, reverse=True)
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
