from json_reader.json_parser import JSONParser
from json_reader.city import CityCollection
from utils.files_definition import FilePaths
from json_reader.autocomplete_helper import AutocompleteHelper


class CityCollectionBuilder:
    default_city_location = FilePaths.DEFAULT_CITIES_FILE

    def __init__(self, default_cities_location=None):
        if default_cities_location:
            self.default_city_location = default_cities_location

    def build(self):
        parser = JSONParser()
        cities_arr = parser.read_cities_from_file(self.default_city_location)
        return CityCollection(cities_arr)

    def build_map(self):
        collection = self.build()
        cities_map = AutocompleteHelper()
        cities_map.load_from(collection)
        return cities_map
