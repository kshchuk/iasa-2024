from json import JSONDecodeError

import pytest

from json_reader.json_reader import JSONReader


def test_json_reader_ok():
    city_list = JSONReader.read_file("resource/test/test-city.json")
    assert len(city_list) == 5
    ushuaia = city_list[0]

    assert ushuaia['name'] == "Ushuaia"
    assert ushuaia['country'] == "Argentina"
    assert ushuaia['id'] == 1

    grytviken = city_list[1]

    assert grytviken['name'] == "Grytviken"
    assert grytviken['state'] == "South Georgia and the South Sandwich Islands"
    assert grytviken['id'] == 2


def test_json_reader_invalid():
    with pytest.raises(FileNotFoundError):
        JSONReader.read_file("resource/test/NO_SUCH_FILE")
    with pytest.raises(JSONDecodeError):
        JSONReader.read_file("resource/test/invalid-json.json")
