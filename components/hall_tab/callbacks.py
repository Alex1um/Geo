from components.hall_tab import START_BUTTON, START_COMPONENT, HALL_PLOTS, HALL_GRAPH, RANGE_GRAPH, HALL_PROCESS_BT
from components.main_page import MAIN_TABLE
from dash_app import app
from dash import Input, Output, State, dcc
import pandas as pd
import plotly.graph_objects as go
from holla import makeHolla


@app.callback(
    [
        Output(START_COMPONENT, "className"),
        Output(HALL_PLOTS, "className"),
        Output(RANGE_GRAPH, "figure"),
    ],
    [
        Input(START_BUTTON, "n_clicks"),
    ],
    [
        State(MAIN_TABLE, "derived_virtual_data"),
        State(START_COMPONENT, "className"),
        State(HALL_PLOTS, "className"),
    ],
    prevent_initial_call=True,
)
def on_start(_, data, class_start: str, class_hall: str):

    dataframe = pd.DataFrame(data)
    dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime)
    dataframe = dataframe.set_index("DATE").sort_index()

    data = [
        go.Scatter(x=dataframe.index, y=dataframe[col], mode="lines", name=col)
        for col in dataframe.columns
    ]
    layout = go.Layout(hovermode="closest",
                        title="<b>0</b>",
                        yaxis={"title": "<b>1<b>"},
                        xaxis=dict(
                            title="<b>2</b>",
                            rangeslider=dict(
                                visible=True
                            )
                        ),
                        legend={"title": "3"},
                        )
    fig = go.Figure(data, layout)
    
    return [
        class_start.replace("d-flex", "d-none"),
        class_hall.replace("d-none", "d-flex"),
        fig,
    ]


@app.callback(
    [
        Output(HALL_GRAPH, "figure")
    ],
    [
        Input(HALL_PROCESS_BT, "n_clicks")
    ],
    [
        State(RANGE_GRAPH, "figure"),
        State(MAIN_TABLE, "derived_virtual_data"),
    ],
    prevent_initial_call=True,
)
def on_process(_, fig, data):

    dataframe = pd.DataFrame(data)
    dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime)
    dataframe = dataframe.set_index("DATE").sort_index()[["P", "Q", "P_0"]]

    data_range = fig["layout"]["xaxis"]["range"]
    if "W" not in dataframe:
        dataframe = makeHolla(dataframe)
    df = dataframe[data_range[0]: data_range[1]]
    return [{
        'data': [
            {'x': df["W"], 'y': df["HI"], 'type': 'line', 'name': 'HI'},
            {'x': df["W"][0:-1], 'y': df["DHI"][0:-1], 'type': 'line', 'name': 'DHI'},
        ],
        'layout': {
            'title': 'График Холла'
        }
    }]



