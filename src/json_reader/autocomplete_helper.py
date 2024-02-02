from json_reader.city import CityCollection, CityInfo

from math import radians, cos, sin, sqrt, atan2


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

    def find_first_n(self, target_string, n=10):
        target_lower = target_string.lower()
        strings = self.all_keys()
        matching_strings = [string for string in strings if target_lower in string.lower()]
        return matching_strings[:n]

    def find_closest(self, lat, lon):
        closest_city = None
        min_distance = float('inf')

        for city_name in self.map.keys():
            city = self.map[city_name]
            distance = self.haversine(lat, lon, city.lat, city.lon)
            if distance < min_distance:
                closest_city = city_name
                min_distance = distance

        return closest_city

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        radi = 6371.0

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = radi * c

        return distance
