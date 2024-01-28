

class CityInfo:
    def __init__(self, id, name, findname, country, coord):
        self.id = id
        self.name = name
        self.findname = findname
        self.country = country
        self.coord = coord

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, FindName: {self.findname}, Country: {self.country}, Coordinates: {self.coord}"


class CountryInfo:
    def __init__(self, name, tag, region):
        self.name = name
        self.tag = tag
        self.region = region
        self.cities = []


class WorldMap:
    continents_map = {}

    def __init__(self, continents_map=None):
        if continents_map:
            self.continents_map = continents_map

    def get_countries_by_continent(self, continent):
        return self.continents_map[continent]

    def get_cities_by_country(self, continent: str, country_name: str):
        cities = self.continents_map[continent][country_name]
        names = [t.name for t in cities.values()]
        return names



