from ipyleaflet import Map, Marker

import panel as pn

pn.extension("ipywidgets", sizing_mode="stretch_width")

ACCENT_BASE_COLOR = "#DAA520"


def get_marker_and_map():
    center = (52.204793, 360.121558)

    lmap = Map(center=center, zoom=15, height=500)

    marker = Marker(location=center, draggable=True)
    lmap.add(marker)
    lmap.layout.height = "100%"
    lmap.layout.width = "100%"
    return marker, lmap


marker, lmap = get_marker_and_map()

json_widget = pn.pane.JSON({}, height=75)


def on_location_changed(event):
    new = event["new"]
    json_widget.object = {"x": new[0], "y": new[1]}


marker.observe(on_location_changed, 'location')

component = pn.Column(
    pn.panel(lmap, sizing_mode="stretch_both", min_height=500),
    json_widget
)

template = pn.template.FastListTemplate(
    title="IPyLeaflet",
    logo="https://panel.holoviz.org/_static/logo_stacked.png",
    header_background=ACCENT_BASE_COLOR,
    accent_base_color=ACCENT_BASE_COLOR,
    main=[component],
).servable()
