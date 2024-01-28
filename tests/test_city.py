from json_reader.builder import WorldMapBuilder


def test_gets_countries():
    builder = WorldMapBuilder()
    world_map = builder.build()
    assert world_map
    assert len(world_map.continents_map) > 0

    europe = world_map.get_countries_by_continent("Europe")
    assert "Ukraine" in europe
    assert "France" in europe
    assert "Albania" in europe

    asia = world_map.get_countries_by_continent("Asia")
    assert "China" in asia
    assert "Japan" in asia


def test_gets_cities():
    builder = WorldMapBuilder()
    world_map = builder.build()
    assert world_map
    assert len(world_map.continents_map) > 0

    ukraine = world_map.get_cities_by_country("Europe", "Ukraine")
    assert "Kiev" in ukraine
    assert "Lviv" in ukraine
    assert "Poltava" in ukraine
