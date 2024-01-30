from json_reader.json_parser import JSONParser
from json_reader.builder import CityCollectionBuilder

from utils.files_definition import FilePaths


def test_parse_cities():
    parser = JSONParser()
    cities = parser.read_cities_from_file(FilePaths.TEST_CITIES_FILE)
    validate_cities(cities)


def test_city_collection_builder():
    builder = CityCollectionBuilder(FilePaths.TEST_CITIES_FILE)
    collection = builder.build()
    validate_cities(collection.cities)


def validate_cities(cities):
    assert len(cities) == 5
    ushuaia = cities[0]
    validate_first_city(ushuaia)


def validate_first_city(city):
    assert city.id == 1
    assert city.name == "Ushuaia"
    assert city.country == "Argentina"
    assert city.state == "Argentina, Tierra del Fuego"
    assert city.lat == -54.799999
    assert city.lon == -68.300003
    assert city.population == 56825


def test_search_by_id():
    collection = create_collection()
    ushuaia = collection.get_city_by_id(1)
    validate_first_city(ushuaia)


def create_collection():
    return CityCollectionBuilder(FilePaths.TEST_CITIES_FILE).build()


def test_get_all():
    collection = create_collection()
    assert len(collection.get_all()) == 5
