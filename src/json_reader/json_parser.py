from json_reader.json_reader import JSONReader

from json_reader.city import CityInfo


class JSONParser:

    def read_cities_from_file(self, filename):
        data = JSONReader.read_file(filename)
        return self._parse_to_cities(data)

    def _parse_to_cities(self, json_data):
        city_infos = []
        for c in json_data:
            id = c['id']
            name = c['name']
            country = c['country']
            state = c['state']
            lat = c['lat']
            lon = c['lon']
            population = c['population']
            city_info = CityInfo(id, name, country, state, lat, lon, population)
            city_infos.append(city_info)
        return city_infos



