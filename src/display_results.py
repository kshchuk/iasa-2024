import panel as pn
from typing import List
import pandas as pd
from dynamic import DynamicContentHolder
import matplotlib.pyplot as plt


def display_mock_data():
    actual_weather = [
        {
            "temperature": 30,
            "pressure": 20,
            "wind_speed": 10,
            "date": "2022-01-01",
            "type": "clear"
        },
        {
            "temperature": 31,
            "pressure": 21,
            "wind_speed": 11,
            "date": "2022-01-02",
            "type": "clear"
        },
        {
            "temperature": 32,
            "pressure": 22,
            "wind_speed": 12,
            "date": "2022-01-03",
            "type": "clear"
        },
    ]
    predicted_weather = [
        {
            "temperature": 32,
            "pressure": 22,
            "wind_speed": 12,
            "date": "2022-01-01",
            "type": "clear"
        },
        {
            "temperature": 31,
            "pressure": 21,
            "wind_speed": 11,
            "date": "2022-01-02",
            "type": "cloudy"
        },
        {
            "temperature": 30,
            "pressure": 20,
            "wind_speed": 10,
            "date": "2022-01-03",
            "type": "clear"
        },
    ]
    return build_results_widget(actual_weather, predicted_weather,
                                ["temperature", "pressure", "wind_speed", "type"],
                                ["Temperature", "Pressure", "Wind Speed", "Weather Type"])


def build_results_widget(actual_weather, predicted_weather, use_columns: List[str],
                         column_names: List[str], date_column='date'):
    """

    :param actual_weather: list of dictionaries/dataframes, historical weather
    :param predicted_weather: list of dictionaries/dataframes, predicted weather,
    must be the same length as actual_weather
    :param use_columns: columns to be displayed on the graph and the result list
    :param column_names: pretty names for columns in the same order as use_columns
    :return: tuple (ListWidget, GraphWidget)
    """
    if len(actual_weather) != len(predicted_weather):
        raise ValueError("actual_weather and predicted_weather lengths do not match")

    if len(use_columns) != len(column_names):
        raise ValueError("use_columns and column_names lengths do not match")

    list_widget = _build_result_list_widget(actual_weather, predicted_weather, use_columns, column_names, date_column)
    plots_widget = _build_plots_widget(actual_weather, predicted_weather, use_columns, column_names, date_column)
    return list_widget, plots_widget


def _to_pretty_row(pretty_name, actual_value, predicted_value):
    return _colored_rectangles([pretty_name, actual_value, predicted_value],
                               ["green", "orange", "#27B4BE"])


def _colored_rectangles(words, colors):
    rectangles = []

    for word, color in zip(words, colors):
        markdown = pn.pane.Markdown(
            f"""<div 
               style='background-color:{color}; color:white; border-radius:10px; padding:10px; text-align:center'>{word}
               </div>""",
            width=100, height=50, sizing_mode="fixed")
        rectangles.append(markdown)

    return pn.FlexBox(*rectangles).clone(flex_wrap='nowrap', flex_direction='row')


def _create_plot_matplot(dates, column_actual_data, column_predicted_data, title):
    fig, ax = plt.subplots()
    ax.plot(dates, column_predicted_data, label='Predicted', marker='o')
    ax.plot(dates, column_actual_data , label='Actual', linestyle='--', marker='x')
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.legend()
    return fig


def _build_result_list_widget(actual_weather, predicted_weather, use_columns, column_names, date_column):
    def_styles = """
        <style>
            table {
                border-collapse: separate;
                border-spacing: 0;
                width: 100%;
                table-layout: fixed; /* Makes table layout more flexible */
            }
            th, td {
                padding: 8px;
                text-align: left;
                border-radius: 8px; /* Rounded corners for cells */
                border: 1px solid #ccc;
            }
           
        </style>
        """

    # Starting the HTML table with styles included
    html = def_styles + '<table>'
    html += ('<tr><th>Date</th><th>Parameter</th>'
             '<th style="color:green">Actual</th><th style="color:#dd0000">Predicted</th>'
             '</tr>')
    for (_, actual_w), (_, predicted_w) in zip(actual_weather.iterrows(), predicted_weather.iterrows()):
        date_rowspan = f'rowspan="{len(column_names) + 1}"'

        html += f'<tr><td {date_rowspan} style="vertical-align: middle;"><b>{actual_w["date"]}</b></td></tr>'
        for column_name, pretty_name in zip(use_columns, column_names):
            html += '<tr>'
            html += f'<td>{pretty_name}</td>'
            html += f'<td>{actual_w[column_name]}</td>'
            html += f'<td>{predicted_w[column_name]}</td>'
            html += '</tr>'

    html += '</table>'
    return html


def _replace_plot(event, dynamic_plot, plots):
    if not event:
        return
    option = event.new
    if option not in plots:
        return
    dynamic_plot.set_content(plots[option])


def _build_plots_widget(actual_weather, predicted_weather, use_columns, column_names, date_column):
    plots = {}
    dates = _extract_column(actual_weather, date_column)
    options = column_names
    for column_name, pretty_name in zip(use_columns, column_names):
        column_actual_data = _extract_column(actual_weather, column_name)
        column_predicted_data = _extract_column(predicted_weather, column_name)
        plot = _create_plot_matplot(dates, column_actual_data, column_predicted_data, pretty_name)
        plots[pretty_name] = plot
    dynamic_plot = DynamicContentHolder()
    select_plot = pn.widgets.Select(options=options)
    select_plot = select_plot.clone(margin=25)
    widget = pn.Column(
        select_plot,
        dynamic_plot.get_holder()
    )
    if len(plots) > 0:
        select_plot.param.watch(lambda event: _replace_plot(event, dynamic_plot, plots), 'value')
        select_plot.value = options[0]
        dynamic_plot.set_content(plots[options[0]])
    return widget


def _create_plot(dates, actual_data, predicted_data, title):
    data = pd.DataFrame({
        'Date': dates,
        'Actual': actual_data,
        'Predicted': predicted_data
    })

    data = data.set_index('Date')

    plot = data.hvplot.line(
        y=['Actual', 'Predicted'],
        width=800,
        height=400,
        xlabel='Date',
        ylabel='Value',
        title=title
    )
    return pn.panel(plot)


def _extract_column(weather_set: pd.DataFrame, column_name: str):
    return weather_set[column_name].tolist()
