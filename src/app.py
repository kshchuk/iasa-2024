import traceback

import panel.widgets
from ipyleaflet import Map
import panel as pn
import difflib
from json_reader.autocomplete_helper import AutocompleteHelper
from json_reader.builder import CityCollectionBuilder

pn.extension("ipywidgets", sizing_mode="stretch_width")

ACCENT_BASE_COLOR = "#DAA520"





class MapViewer:
    def __init__(self):
        self.map = None
        self.json_widget = None
        self.current_points = (0, 0)
        self.create_map()
        self.create_widgets()
        self.setup_interaction()

    def create_map(self):
        center = (50.45, 30.52)
        self.map = Map(center=center, zoom=5, height=500)
        self.map.layout.height = "100%"
        self.map.layout.width = "100%"

    def create_widgets(self):
        self.json_widget = pn.pane.JSON({}, height=75)

    def setup_interaction(self):
        self.map.on_interaction(self.handler)

    def handler(self, **kwargs):
        if kwargs.get('type') == 'click':
            latlon = kwargs.get('coordinates')
            Map.default_style = {'cursor': 'wait'}
            self.current_points = latlon
            self.json_widget.object = {"x": self.current_points[0],
                                       "y": self.current_points[1]}
            Map.default_style = {'cursor': 'pointer'}

class SearchBox:
    affected_map = None
    autocomplete_helper = None

    def __init__(self, autocomplete_helper: AutocompleteHelper, affected_map:MapViewer=None):
        self.autocomplete_helper = autocomplete_helper
        self.affected_map = affected_map
        self.search_field = panel.widgets.AutocompleteInput(
            name='City', options=autocomplete_helper.all_keys(),
            case_sensitive=False, search_strategy='includes',
            placeholder='Search city',
            min_characters=2
        )
        self.search_field.param.watch(self.update_options, 'value', onlychanged=False)

    def update_options(self, event):
        current_input = event.new
        if current_input== '':
            return
        city = autocomplete_helper.find_by_key(current_input)
        if self.affected_map:
            self.affected_map.map.center = (city.lat, city.lon)
def init_autocomplete_helper():
    try:
        return CityCollectionBuilder().build_map()
    except Exception as e:
        print("Error while creating AutoCompleteHelper:", e)
        traceback.print_exc()
        return AutocompleteHelper()


map_viewer = MapViewer()
autocomplete_helper = init_autocomplete_helper()
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
    title="IPyLeaflet",
    logo="https://panel.holoviz.org/_static/logo_stacked.png",
    header_background=ACCENT_BASE_COLOR,
    accent_base_color=ACCENT_BASE_COLOR,
    main=[main_component],
).servable()
