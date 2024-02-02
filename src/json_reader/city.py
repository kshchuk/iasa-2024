

class CityInfo:
    def __init__(self, id, name, country, state, lat, lon, population):
        self.id = id
        self.name = name
        self.country = country
        self.state = state
        self.lat = lat
        self.lon = lon
        self.population = population

    def __str__(self) -> str:
        return f"ID: {self.id}, Name: {self.name}, State: {self.state}, Population: {self.population}"


class CityCollection:
    cities: list[CityInfo] = []

    def __init__(self, cities=None):
        if cities:
            self.cities = cities

    def set_cities(self, cities) -> None:
        self.cities = cities

    def get_city_by_id(self, id: int) -> CityInfo:
        return self.cities[id-1]

    def get_all(self) -> list[CityInfo]:
        return self.cities



