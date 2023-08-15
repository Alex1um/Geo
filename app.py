import copy

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import pyfunc, pylayout, pylayoutfunc
from dash import dcc, html, Input, Output, State
from pathlib import Path
import plotly.graph_objects as go
from dash import dash_table
import numpy as np
from holla import makeHolla
from typing import Callable
import base64
import io


dataframe_source: tuple[bytes, Callable] = None
dataframe: pd.DataFrame = None


# APP
app = dash.Dash(
    suppress_callback_exceptions=False,
    external_stylesheets=[getattr(dbc.themes, "COSMO"), "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"],
)
server = app.server

app.layout = dbc.Container(
    [
        pylayout.HTML_TITLE,
        pylayout.HTML_ROW_BUTTON_UPLOAD,
        pylayout.TABLE_CONFIG,
        pylayout.HTML_ROW_TABLE,
        pylayout.HTML_ROW_BUTTON_VIZ,
        pylayout.HTML_ROW_GRAPH_ONE,
    ],
    fluid=True,
    className="dbc",
)

@app.callback(
    [
        Output("table-config", "style"),
        Output("select-start", "value"),
        Output("row-table-uploaded", "children"),
        # Output("button-visualize", "disabled"),
        # Output("button-visualize", "outline"),
    ],
    Input("dcc-upload", "contents"),
    State("dcc-upload", "filename"),
    State("dcc-upload", "last_modified"),
    Input("button-skip", "n_clicks"),
    prevent_initial_call=True,
)
def callback_upload(content, filename, filedate, _):
    global dataframe_source, dataframe

    dataframe_source = None

    if content is not None:
        _, content_string = content.split(",")

        decoded = base64.b64decode(content_string)

        if filename.endswith(".csv"):
            dataframe_source = (io.StringIO(decoded.decode("utf-8")), pd.read_csv)
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            dataframe_source = (decoded, pd.read_excel)

    # button_viz_disabled = True
    # button_viz_outline = True

    val = -1
    disabled = {"visibility": "hidden"}
    children = []

    if dataframe_source is not None:
        disabled["visibility"] = "visible"
        val = 0
        dataframe_source = dataframe_source
        dataframe = dataframe_source[1](dataframe_source[0], parse_dates=[[0, 1]])

        editable = [False] + [True] * len(dataframe.columns)
        children = pylayoutfunc.create_table_layout(
            dataframe,
            "output-table",
            filename=filename,
            filedate=filedate,
            editable=editable,
            renamable=True,
        )
        # button_viz_disabled = False
        # button_viz_outline = False
    else:
        children = "Error!"

    return [
        disabled,
        val,
        children,
        # button_viz_disabled,
        # button_viz_outline,
    ]


@app.callback(
    [
        Output("select-t", "options"),
        Output("select-q", "options"),
        Output("select-p", "options"),
        Output("select-p0", "options"),
    ],
    Input("select-start", "value"),
    prevent_initial_call=True,
)
def callback_start(value: int):
    global dataframe
    cols = []
    if value >= 0:
        if value == 0:
            cols = dataframe.columns.array
        else:
            cols = dataframe.iloc[value - 1]
    return [
        cols,
        cols,
        cols,
        cols,
    ]


@app.callback(
    [
        Output("graph-container", "children"),
    ],
    Input("button-visualize", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
    State("graph-selector", "value"),
    prevent_initial_call=True,
)
def callback_visualize(_, table_data, table_columns, graph_selector):
    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

    children = []

    if graph_selector == "Hall":
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
        main_graph = dcc.Graph(figure=fig, id="graph-hall-data")
        children.append(main_graph)
        children.append(dbc.Button(children="Process", id="bt-hall", color="primary", outline=False, className="fs-4 text-center"))
        children.append(dcc.Graph(id="hall-graph"))
    elif graph_selector == "SRT":
        data = [
            go.Scatter(x=dataframe.index, y=dataframe[col], mode="lines", name=col)
            for col in dataframe.columns
        ]
        selected_points = go.Scatter(x=[], y=[], mode="markers", name="selected", marker={"color": "#00ff00", "size": 20})
        data.append(selected_points)
        layout = go.Layout(hovermode="closest",
                           title="<b>0</b>",
                           yaxis={"title": "<b>1<b>"},
                           xaxis={"title": "<b>2</b>"},
                           legend={"title": "3"},
                           )
        fig = go.Figure(data, layout)
        main_graph = dcc.Graph(figure=fig, id="graph-srt-data")

        layout_regression = go.Layout(hovermode="closest",
                           title="<b>0</b>",
                           yaxis={"title": "<b>1<b>"},
                           xaxis={"title": "<b>2</b>"},
                           legend={"title": "3"},
                           )
        regr_line = go.Scatter(x=[], y=[], mode="lines", name="regression")
        fig = go.Figure([selected_points, regr_line], layout_regression)
        regr_graph = dcc.Graph(figure=fig, id="graph-srt-regr-data")

        children = [main_graph, regr_graph]

    return [
        children,
    ]

@app.callback(
    [
        Output("graph-srt-data", "figure"),
        Output("graph-srt-regr-data", "figure"),
    ],
    [Input("graph-srt-data", "clickData")],
    [
        State("graph-srt-data", "figure"),
        State("graph-srt-regr-data", "figure")
    ],
    prevent_initial_call=True,
)
def on_graph_click(clickData, fig: dict, regr_fig: dict):
    curves = len(fig['data'])
    if clickData:
        new_x, new_y = clickData['points'][0]['x'], clickData['points'][0]['y']
        y: list = fig['data'][-1]['y']
        x: list = fig['data'][-1]['x']
        if clickData['points'][0]['curveNumber'] != curves - 1:
            y.append(new_y)
            x.append(new_x)
        else:
            i = x.index(new_x)
            x.pop(i)
            y.pop(i)

        regr_fig['data'][0]['y'] = y
        regr_fig['data'][0]['x'] = x

        x_len = len(x)

        A = np.vstack([np.array(range(x_len)), np.ones(x_len)]).T
        m, c = np.linalg.lstsq(A, np.array(y), rcond=None)[0]

        regr_fig['data'][1]['x'] = [min(x), max(x)]
        regr_fig['data'][1]['y'] = [c, m * (x_len - 1) + c]

    return fig, regr_fig


@app.callback(
    [
        Output("graph-hall-data", "figure"),
        Output("hall-graph", "figure")
    ],
    [Input("bt-hall", "n_clicks")],
    [State("graph-hall-data", "figure")],
    prevent_initial_call=True,
)
def on_graph_select(bt, fig: dict):
    global dataframe
    data_range = fig["layout"]["xaxis"]["range"]
    if "W" not in dataframe:
        dataframe = makeHolla(dataframe)
    df = dataframe[data_range[0] : data_range[1]]
    return [fig, {
        'data': [
            {'x': df["W"], 'y': df["HI"], 'type': 'line', 'name': 'HI'},
            {'x': df["W"][0:-1], 'y': df["DHI"][0:-1], 'type': 'line', 'name': 'DHI'},
        ],
        'layout': {
            'title': 'График Холла'
        }
    }]


if __name__ == "__main__":
    app.run_server(debug=True)
