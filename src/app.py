import traceback

import panel.widgets
from ipyleaflet import Map
import panel as pn

import datetime
from json_reader.autocomplete_helper import AutocompleteHelper
from json_reader.builder import CityCollectionBuilder
from display_results import display_mock_data
from dynamic import DynamicContentHolder

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
        self.search_box_ref = None

    def update_map(self, latitude, longitude):
        self.current_point = (latitude, longitude)
        self.json_widget.object = {"x": self.current_point[0],
                                   "y": self.current_point[1]}
        if self.search_box_ref:
            self.search_box_ref.forced_change(
                self.search_box_ref.autocomplete_helper.find_closest(latitude, longitude))

    def handler(self, **kwargs):
        if kwargs.get('type') == 'click':
            latlon = kwargs.get('coordinates')
            self.update_map(latlon[0], latlon[1])

    def set_search_box_ref(self, search_box_ref):
        self.search_box_ref = search_box_ref


class SearchBox:
    affected_map = None
    autocomplete_helper = None

    def __init__(self, autocomplete_helper_arg: AutocompleteHelper,
                 affected_map: MapViewer = None, limit=10):
        self.autocomplete_helper = autocomplete_helper_arg
        self.affected_map = affected_map
        self.limit = limit
        self.forced = False
        self.search_field = panel.widgets.AutocompleteInput(
            name='City', options=[],
            case_sensitive=False, search_strategy='includes',
            placeholder='Search city',
            min_characters=2
        )
        self.search_field.param.watch(self.update_options, 'value',
                                      onlychanged=False)
        self.search_field.param.watch(self.on_input_update, 'value_input',
                                      onlychanged=False)

    def update_options(self, event):
        current_input = event.new
        if current_input == '' or self.forced:
            return
        city = self.autocomplete_helper.find_by_key(current_input)
        if self.affected_map:
            self.affected_map.map.center = (city.lat, city.lon)
            self.affected_map.map.zoom = 8
            self.affected_map.update_map(city.lat, city.lon)

    def on_input_update(self, event):
        if not event:
            return
        current_input = event.new
        if current_input == '':
            self.search_field.options = []
        new_options = self.autocomplete_helper.find_first_n(current_input, n=self.limit)
        self.search_field.options = new_options

    @staticmethod
    def init_autocomplete_helper():
        try:
            return CityCollectionBuilder().build_map()
        except Exception as e:
            print("Error while creating AutoCompleteHelper:", e)
            traceback.print_exc()
            return AutocompleteHelper()

    def forced_change(self, option):
        self.forced = True
        self.search_field.value = option
        self.forced = False


class OptionsBox:
    def __init__(self):
        current_date = datetime.date.today()
        common_width = 150
        common_height = 50

        seven_days_ago = current_date - datetime.timedelta(days=7)
        self.from_date_picker = pn.widgets.DatePicker(name='From', end=current_date, value=seven_days_ago,
                                                      width=common_width, height=common_height)
        self.to_date_picker = pn.widgets.DatePicker(name='To', end=current_date, value=current_date,
                                                    width=common_width, height=common_height)
        self.prediction_type = pn.widgets.Select(name='Type', options=['Daily', 'Hourly'],
                                                 width=common_width, height=common_height)
        self.submit_btn = pn.widgets.Button(name='Predict', button_type='primary',
                                            width=common_width, height=common_height)
        temp_flex = pn.FlexBox(
            self.from_date_picker,
            self.to_date_picker,
            self.prediction_type,
            self.submit_btn
        )
        self.options_row = temp_flex.clone(flex_direction='row', align_items='flex-end', justify_content='center')

    def collect_data(self):
        return {
            'from': self._format_date_value(self.from_date_picker),
            'to': self._format_date_value(self.to_date_picker),
            'type': self.prediction_type.value
        }

    def _format_date_value(self, date_picker: pn.widgets.DatePicker):
        selected_date = date_picker.value
        return selected_date.strftime('%Y-%m-%d') if selected_date else ''

    def set_on_predict_btn_pressed(self, runnable):
        if not callable(runnable):
            raise ValueError("Cannot call the runnable argument")
        pn.bind(runnable, self.submit_btn, watch=True)


class UserInputCollector:
    def __init__(self, def_map_viewer: MapViewer, def_options_box: OptionsBox):
        self.map_viewer = def_map_viewer
        self.options_box = def_options_box

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
map_viewer.set_search_box_ref(search_box)
options_box = OptionsBox()

result_list = DynamicContentHolder()
graphs_list = DynamicContentHolder()


def build_weather_forecast(event):
    if not event:
        return
    user_input = UserInputCollector.collect_user_input(map_viewer, options_box)
    print(user_input)  # Use in weather forecast
    list_widget, plots_widget = display_mock_data()
    result_list.set_content(list_widget)
    graphs_list.set_content(plots_widget)


options_box.set_on_predict_btn_pressed(build_weather_forecast)

map_component = pn.Column(
    pn.panel(map_viewer.map, sizing_mode="stretch_both", min_height=500),
    map_viewer.json_widget
)
left_pane = pn.Column(
    map_component, graphs_list.get_holder()
)

inputs_component = pn.Column(
    pn.Row(search_box.search_field, height=100),
    pn.Row(options_box.options_row, height=100),
    result_list.get_holder()
)
main_component = pn.Row(
    left_pane, inputs_component
)

template = pn.template.FastListTemplate(
    title="WeatherCast",
    logo="https://i.imgur.com/7NenPSk.png",
    header_background=ACCENT_BASE_COLOR,
    accent_base_color=ACCENT_BASE_COLOR,
    main=[main_component],
).servable()
