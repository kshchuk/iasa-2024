from src.json_reader.json_reader import JSONReader
import pytest


def test_json_reader_ok():
    city_list = JSONReader.read_cities_from_file("resource/test/test-city.json")
    assert len(city_list) == 4
    kiev = city_list[0]

    assert kiev.name == "Kiev"
    assert kiev.findname == "KIEV"
    assert kiev.coord == {
        "lon": 30.516666,
        "lat": 50.433334
    }
    assert kiev.country == "UA"
    assert kiev.id == 703448


def test_json_reader_invalid_data():
    with pytest.raises(KeyError):
        JSONReader.read_cities_from_file("resource/test/invalid-city.json")
