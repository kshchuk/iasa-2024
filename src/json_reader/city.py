class CityInfo:
    def __init__(self, id, name, findname, country, coord):
        self.id = id
        self.name = name
        self.findname = findname
        self.country = country
        self.coord = coord

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, FindName: {self.findname}, Country: {self.country}, Coordinates: {self.coord}"


class WorldMap:

    def get_countries_by_continent(self, continent):
        return 0

    def get_cities_by_country(self, country):
        return 0
