from json_reader.json_parser import JSONParser
from json_reader.builder import CityCollectionBuilder

def test_parse_cities():
    parser = JSONParser()
    cities = parser.read_cities_from_file("resource/test/test-city.json")
    assert len(cities) == 5

    ushuaia = cities[0]

    assert ushuaia.id == 1
    assert ushuaia.name == "Ushuaia"
    assert ushuaia.country == "Argentina"
    assert ushuaia.state == "Argentina, Tierra del Fuego"
    assert ushuaia.lat == -54.799999
    assert ushuaia.lon == -68.300003
    assert ushuaia.population == 56825
