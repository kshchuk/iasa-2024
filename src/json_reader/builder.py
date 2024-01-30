from json_parser import JSONParser
from city import CityInfo
from city import CountryInfo
from city import WorldMap


class WorldMapBuilder:
    default_city_location = "resource/cities/history-city-list.json"

    def __init__(self, default_continents_location=None, default_cities_location=None):
        if default_continents_location:
            self.default_continents_location = default_continents_location
        if default_cities_location:
            self.default_city_location = default_cities_location

    def build(self):
        parser = JSONParser()
        cities = parser.read_cities_from_file(self.default_city_location)
        countries = parser.read_countries_and_continents_from_file(self.default_continents_location)
        w_map = {}
        for city in cities:
            tag = city.country
            country = countries[tag]
            continent = country.region
            self._merge(w_map, continent, country, city)

        return WorldMap(w_map)

    def _merge(self, w_map: dict, continent: str, country: CountryInfo, city: CityInfo):
        countries_map = {}
        if continent in w_map:
            countries_map = w_map[continent]
        else:
            w_map[continent] = countries_map

        city_map = {}
        if country.name in countries_map:
            city_map = countries_map[country.name]
        else:
            countries_map[country.name] = city_map
        city_map[city.findname] = city
