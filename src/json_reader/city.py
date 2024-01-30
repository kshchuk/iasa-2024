

class CityInfo:
    def __init__(self, id, name, country, state, lat, lon, population):
        self.id = id
        self.name = name
        self.country = country
        self.state = state
        self.lat = lat
        self.lon = lon
        self.population = population

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, State: {self.state}, Population: {self.population}"


class CityCollection:
    cities = []

    def __init__(self, cities=None):
        if cities:
            self.cities = cities

    def set_cities(self, cities):
        self.cities = cities

    def get_city_by_id(self, id: int):
        size = len(self.cities)
        if id > size:
            raise IndexError(f"Cannot get city by id {id}. Max id = {size}")
        return self.cities[id - 1]



