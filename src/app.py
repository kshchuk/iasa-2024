import traceback

import panel.widgets
from ipyleaflet import Map
import panel as pn

from json_reader.autocomplete_helper import AutocompleteHelper
from json_reader.builder import CityCollectionBuilder

pn.extension("ipywidgets", sizing_mode="stretch_width")

ACCENT_BASE_COLOR = "#DAA520"


class MapViewer:
    start_point: tuple[int, int] = (50.45, 30.52)

    def __init__(self):
        self.map: Map = Map(center=self.start_point, zoom=5, height=500,
                            scroll_wheel_zoom=True)
        self.json_widget: pn.pane.JSON = pn.pane.JSON({}, height=75)
        self.current_point: tuple[int, int] = (0, 0)

        self.map.layout.height = "100%"
        self.map.layout.width = "100%"
        self.map.on_interaction(self.handler)

    def update_map(self, latitude, longitude):
        self.current_point = (latitude, longitude)
        self.json_widget.object = {"x": self.current_point[0],
                                   "y": self.current_point[1]}

    def handler(self, **kwargs):
        if kwargs.get('type') == 'click':
            latlon = kwargs.get('coordinates')
            self.update_map(latlon[0], latlon[1])


class SearchBox:
    affected_map = None
    autocomplete_helper = None

    def __init__(self, autocomplete_helper: AutocompleteHelper,
                 affected_map: MapViewer = None):
        self.autocomplete_helper = autocomplete_helper
        self.affected_map = affected_map
        self.search_field = panel.widgets.AutocompleteInput(
            name='City', options=autocomplete_helper.all_keys(),
            case_sensitive=False, search_strategy='includes',
            placeholder='Search city',
            min_characters=2
        )
        self.search_field.param.watch(self.update_options, 'value',
                                      onlychanged=False)

    def update_options(self, event):
        current_input = event.new
        if current_input == '':
            return
        city = autocomplete_helper.find_by_key(current_input)
        if self.affected_map:
            self.affected_map.map.center = (city.lat, city.lon)
            self.affected_map.map.zoom = 8
            self.affected_map.update_map(city.lat, city.lon)

    @staticmethod
    def init_autocomplete_helper():
        try:
            return CityCollectionBuilder().build_map()
        except Exception as e:
            print("Error while creating AutoCompleteHelper:", e)
            traceback.print_exc()
            return AutocompleteHelper()


map_viewer = MapViewer()
autocomplete_helper = SearchBox.init_autocomplete_helper()
search_box = SearchBox(autocomplete_helper, map_viewer)

map_component = pn.Column(
    pn.panel(map_viewer.map, sizing_mode="stretch_both", min_height=500),
    map_viewer.json_widget
)

inputs_component = pn.Column(
    pn.Row(search_box.search_field, height=100)
)
main_component = pn.Row(
    map_component, inputs_component
)

template = pn.template.FastListTemplate(
    title="WeatherCast",
    logo="https://i.imgur.com/7NenPSk.png",
    header_background=ACCENT_BASE_COLOR,
    accent_base_color=ACCENT_BASE_COLOR,
    main=[main_component],
).servable()