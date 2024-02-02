import panel as pn
import panel.widgets
from typing import List
import pandas as pd
import hvplot.pandas

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


def _build_result_list_widget(actual_weather, predicted_weather, use_columns, column_names, date_column):
    list_widget = pn.Column()
    list_widget.append(
        _to_pretty_row("<b>Parameter</b>", "<b>Actual</b>", "<b>Predicted</b>")
    )
    for actual_item, predicted_item in zip(actual_weather, predicted_weather):
        title = actual_item[date_column]
        date_declaration = pn.widgets.StaticText(name='Date', value=title)
        column = pn.Column()
        column.append(date_declaration)
        for column_name, pretty_name in zip(use_columns, column_names):
            actual_value = actual_item[column_name]
            predicted_value = predicted_item[column_name]

            row = _to_pretty_row(pretty_name, actual_value, predicted_value)
            column.append(row)
        list_widget.append(column)

    return list_widget


def _build_plots_widget(actual_weather, predicted_weather, use_columns, column_names, date_column):
    plots = pn.Column()
    dates = _extract_column(actual_weather, date_column)
    for column_name, pretty_name in zip(use_columns, column_names):
        column_actual_data = _extract_column(actual_weather, column_name)
        column_predicted_data = _extract_column(predicted_weather, column_name)
        plot = _create_plot(dates, column_actual_data, column_predicted_data, pretty_name)
        plots.append(plot)
    return plots


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


def _extract_column(weather_set, column_name):
    return [ws[column_name] for ws in weather_set]
