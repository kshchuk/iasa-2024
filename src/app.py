from ipyleaflet import Map
import panel as pn

pn.extension("ipywidgets", sizing_mode="stretch_width")

ACCENT_BASE_COLOR = "#DAA520"


class MapViewer:
    def __init__(self):
        self.map = None
        self.json_widget = None
        self.current_points = (0, 0)
        self.create_map()
        self.create_widgets()
        self.interaction = self.setup_interaction()

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


map_viewer = MapViewer()

component = pn.Column(
    pn.panel(map_viewer.map, sizing_mode="stretch_both", min_height=500),
    map_viewer.json_widget
)

template = pn.template.FastListTemplate(
    title="IPyLeaflet",
    logo="https://panel.holoviz.org/_static/logo_stacked.png",
    header_background=ACCENT_BASE_COLOR,
    accent_base_color=ACCENT_BASE_COLOR,
    main=[component],
).servable()
