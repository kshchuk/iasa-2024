from src.json_reader.json_parser import JSONParser
from src.json_reader.city import CityCollection


class CityCollectionBuilder:
    default_city_location = "resource/cities/cities.json"

    def __init__(self, default_cities_location=None):
        if default_cities_location:
            self.default_city_location = default_cities_location

    def build(self):
        parser = JSONParser()
        cities = parser.read_cities_from_file(self.default_city_location)
        return CityCollection(cities)
