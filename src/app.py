import traceback

import panel.widgets
from ipyleaflet import Map
import panel as pn

import datetime
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


class OptionsBox:
    def __init__(self):
        current_date = datetime.date.today()
        seven_days_ago = current_date - datetime.timedelta(days=7)
        self.from_date_picker = pn.widgets.DatePicker(name='From', end=current_date, value=seven_days_ago)
        self.to_date_picker = pn.widgets.DatePicker(name='To', end=current_date, value=current_date)
        self.prediction_type = pn.widgets.Select(name='Type', options=['Daily', 'Hourly'])
        self.options_row = pn.Row(
            self.from_date_picker,
            self.to_date_picker,
            self.prediction_type
        )

    def collect_data(self):
        return {
            'from': self._format_date_value(self.from_date_picker),
            'to': self._format_date_value(self.to_date_picker),
            'type': self.prediction_type.value
        }

    def _format_date_value(self, date_picker: pn.widgets.DatePicker):
        selected_date = date_picker.value
        return selected_date.strftime('%Y-%m-%d') if selected_date else ''


class UserInputCollector:
    def __init__(self, map_viewer: MapViewer, options_box: OptionsBox):
        self.map_viewer = map_viewer
        self.options_box = options_box

    def user_input(self):
        return UserInputCollector.collect_user_input(self.map_viewer, self.options_box)

    @staticmethod
    def collect_user_input(clt_viewer: MapViewer, clt_options: OptionsBox):
        """

        :param clt_viewer: map viewer to collect input from
        :param clt_options: options box to collect input from
        :return: dictionary, that includes:
        lon = selected point longitude (uses start point in not selected)
        lat = selected point latitude (uses start point in not selected)
        from = start date (yyyy-mm-dd), empty string if not selected
        to = end date (yyyy-mm-dd), empty string if not selected
        type = 'Daily' or 'Hourly'
        """
        collected_input = clt_options.collect_data()
        current_coords = clt_viewer.current_point
        if not current_coords:
            current_coords = map_viewer.start_point
        collected_input["lon"] = current_coords[0]
        collected_input["lat"] = current_coords[1]
        return collected_input


map_viewer = MapViewer()
autocomplete_helper = SearchBox.init_autocomplete_helper()
search_box = SearchBox(autocomplete_helper, map_viewer)
options_box = OptionsBox()

map_component = pn.Column(
    pn.panel(map_viewer.map, sizing_mode="stretch_both", min_height=500),
    map_viewer.json_widget
)

inputs_component = pn.Column(
    pn.Row(search_box.search_field, height=100),
    pn.Row(options_box.options_row, height=100)
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
