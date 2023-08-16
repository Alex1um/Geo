import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import pylayout
from dash import dcc, html, Input, Output, State
from pathlib import Path
import plotly.graph_objects as go
from dash import dash_table
from plotly.subplots import make_subplots
import numpy as np
from holla import makeHolla
from typing import Callable
import base64
import io
from two_tangs import makeTangs


dataframe_source: pd.DataFrame = None
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
        pylayout.TABLE_BEGIN,
        pylayout.HTML_ROW_TABLE,
        pylayout.HTML_ROW_BUTTON_VIZ,
        pylayout.HTML_ROW_GRAPH_ONE,
    ],
    fluid=True,
    className="dbc",
)

@app.callback(
    [
        Output("table-begin", "style"),
        Output("select-start", "value"),
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
    global dataframe_source

    dataframe_source = None

    if content is not None:
        _, content_string = content.split(",")

        decoded = base64.b64decode(content_string)

        if filename.endswith(".csv"):
            dataframe_source = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            dataframe_source = pd.read_excel(decoded)

    val = -1
    disabled = {"visibility": "hidden"}

    if dataframe_source is not None:
        disabled["visibility"] = "visible"
        val = 0

    return [
        disabled,
        val,
    ]


@app.callback(
    [
        Output("table-begin-table", "data"),
        Output("select-date", "options"),
        Output("select-q", "options"),
        Output("select-p", "options"),
        Output("select-p0", "options"),
        Output("select-date", "value"),
        Output("select-q", "value"),
        Output("select-p", "value"),
        Output("select-p0", "value"),
    ],
    Input("select-start", "value"),
    prevent_initial_call=True,
)
def callback_start(value: int):
    global dataframe_source
    data = []
    cols = []
    if value >= 0:
        new_dataframe = dataframe_source.iloc[value:value + 5]
        if value == 0:
            new_dataframe.columns = dataframe_source.columns
        else:
            new_dataframe.columns = dataframe_source.iloc[value - 1]
        cols = new_dataframe.columns.array
        data = new_dataframe.to_dict("records")
    return [
        data,
        cols,
        cols,
        cols,
        cols,
        None,
        None,
        None,
        None,
    ]

@app.callback(
    [
        Output("table-begin-submit", "disabled"),
        Output("table-begin-submit", "outline")
    ],
    [
        Input("select-date", "value"),
        Input("select-q", "value"),
        Input("select-p", "value"),
        Input("select-p0", "value"),
    ],
    [
        State("select-start", "value")
    ],
    prevent_initial_call=True
)
def callback_start_next(date, q_col, p_col, p0_col, table_start):
    disabled = not all((date, q_col, p_col, p0_col))
    outline = disabled
    return [
        disabled,
        outline
    ]


@app.callback(
    [
        Output("row-table-uploaded", "children"),
        Output("button-visualize", "disabled"),
        Output("button-visualize", "outline"),
    ],
    Input("table-begin-submit", "n_clicks"),
    [
        State("select-date", "value"),
        State("select-q", "value"),
        State("select-p", "value"),
        State("select-p0", "value"),
        State("select-start", "value"),
    ],
    prevent_initial_call=True,
)
def callback_on_table_submit(_, date: list[str], q_col: str, p_col: str, p0_col: str, start: int):
    global dataframe, dataframe_source
    dataframe = dataframe_source.iloc[start:]
    dataframe.columns = dataframe_source.iloc[start - 1]
    dataframe = dataframe[[*date, q_col, p_col, p0_col]]
    dataframe["DATE"] = dataframe[date].apply(lambda x: ' '.join(x.astype(str)), axis=1)
    dataframe.drop(date, axis=1, inplace=True)
    dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime)
    dataframe = dataframe.set_index("DATE").sort_index()
    dataframe = dataframe.rename(columns={q_col: "Q", p_col: "P", p0_col: "P_0"})
    dataframe = dataframe.apply(pd.to_numeric, errors="coerce")

    table = dash_table.DataTable(dataframe.to_dict("records"), id="output-table")

    return [
        table,
        False,
        False
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
    # dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

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

        # вторую ось надо сделать здесь https://plotly.com/python/multiple-axes/
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=dataframe.index, y=dataframe["Pressure"], name="yaxis data"),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=dataframe.index, y=dataframe['FlowRate'], name="yaxis2 data", opacity=0.5),
            secondary_y=True,
        )




        # data = [
        #     go.Scatter(x=dataframe.index, y=dataframe[col], mode="lines", name=col)
        #     for col in dataframe.columns
        # ]
        selected_points = go.Scatter(x=[], y=[], mode="markers", name="Selected Points", marker={"color": "#000000", "size": 10, "symbol": "x-thin", "line": {"width": 2}})
        # data.append(selected_points)
        fig.add_trace(
            go.Scatter(x=[], y=[], mode="markers", name="Selected Points", marker={"color": "#000000", "size": 10, "symbol": "x-thin", "line": {"width": 2}}),
            secondary_y=False,
        )
        layout = go.Layout(hovermode="closest",
                           title="<b>Select points</b>",
                           yaxis={"title": "<b>Pressure<b>"},
                           xaxis={"title": "<b>Time</b>"},
                           legend={"title": "Legend"},
                           )
        # fig = go.Figure(data, layout)
        main_graph = dcc.Graph(figure=fig, id="graph-srt-data")

        layout_regression = go.Layout(hovermode="closest",
                           title="<b>SRTest</b>",
                           yaxis={"title": "<b>Pressure<b>"},
                           xaxis={"title": "<b>Flow Rate</b>"},
                           legend={"title": "Legend"},
                           )
        regr_left = go.Scatter(x=[], y=[], mode="lines", name="Left Regression")
        regr_right = go.Scatter(x=[], y=[], mode="lines", name="Right Regression")
        fig = go.Figure([selected_points, regr_left, regr_right], layout_regression)
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

        regr_fig['data'][0]['x'] = x
        regr_fig['data'][0]['y'] = y

        print("y = ", y)
        print('x = ', x)

        # x_len = len(x)
        # A = np.vstack([np.array(range(x_len)), np.ones(x_len)]).T

        y_left, y_right, cross = makeTangs(x, y)

        # m, c = np.linalg.lstsq(A, np.array(y), rcond=None)[0]
        regr_fig['data'][1]['x'] = x
        regr_fig['data'][1]['y'] = y_left

        regr_fig['data'][2]['x'] = x
        regr_fig['data'][2]['y'] = y_right

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
    df = dataframe[data_range[0]: data_range[1]]
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
