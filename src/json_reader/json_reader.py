import json
import os
from pathlib import Path

from json_reader.city import CityInfo


class JSONReader:
    @staticmethod
    def read_cities_from_file(filename):
        BASE_DIR = Path(os.path.abspath(__file__)).resolve().parent.parent.parent.as_posix()

        with Path(f"{BASE_DIR}/" + filename).open("r") as f:
            data = json.load(f)
            return JSONReader._parse_json_data(data)


    @staticmethod
    def _parse_json_data(json_data):
        city_infos = []
        for c in json_data:
            id = c['id']
            city = c['city']
            name = city['name']
            findname = city['findname']
            country = city['country']
            coord = city['coord']
            city_info = CityInfo(id, name, findname, country, coord)
            city_infos.append(city_info)
        return city_infos

