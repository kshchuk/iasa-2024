from src.json_reader.json_parser import JSONParser
from src.json_reader.city import CityCollection
from utils.files_definition import FilePaths

class CityCollectionBuilder:
    default_city_location = FilePaths.DEFAULT_CITIES_FILE

    def __init__(self, default_cities_location=None):
        if default_cities_location:
            self.default_city_location = default_cities_location

    def build(self):
        parser = JSONParser()
        cities_arr = parser.read_cities_from_file(self.default_city_location)
        cities_map = {city.id: city for city in cities_arr}
        return CityCollection(cities_map)
