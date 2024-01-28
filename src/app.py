from ipyleaflet import Map

import panel as pn

pn.extension("ipywidgets", sizing_mode="stretch_width")

ACCENT_BASE_COLOR = "#DAA520"

current_points = 0, 0


def create_map():
    center = (50.45, 30.52)
    map = Map(center=center, zoom=5, height=500)
    map.layout.height = "100%"
    map.layout.width = "100%"
    return map


map = create_map()

json_widget = pn.pane.JSON({}, height=75)


def handler(**kwargs):
    if kwargs.get('type') == 'click':
        latlon = kwargs.get('coordinates')
        Map.default_style = {'cursor': 'wait'}
        json_widget.object = {"x": latlon[0], "y": latlon[1]}
        Map.default_style = {'cursor': 'pointer'}


map.on_interaction(handler)

component = pn.Column(
    pn.panel(map, sizing_mode="stretch_both", min_height=500),
    json_widget
)

template = pn.template.FastListTemplate(
    title="IPyLeaflet",
    logo="https://panel.holoviz.org/_static/logo_stacked.png",
    header_background=ACCENT_BASE_COLOR,
    accent_base_color=ACCENT_BASE_COLOR,
    main=[component],
).servable()
