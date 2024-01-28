from json_reader.json_reader import JSONReader

from json_reader.city import CountryInfo
from json_reader.city import CityInfo


class JSONParser:

    def read_cities_from_file(self, filename):
        data = JSONReader.read_file(filename)
        return self._parse_to_cities(data)

    def _parse_to_cities(self, json_data):
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

    def read_countries_and_continents_from_file(self, filename):
        data = JSONReader.read_file(filename)
        return self._parse_to_counties_and_regions(data)

    def _parse_to_counties_and_regions(self, json_data):
        tag_to_country_map = {}
        for country in json_data:
            name = country['name']
            tag = country['alpha-2']
            region = country['region']
            country = CountryInfo(name, tag, region)
            tag_to_country_map[tag] = country
        return tag_to_country_map

