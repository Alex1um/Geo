import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import pyfunc, pylayout, pylayoutfunc
from dash import dcc, html, Input, Output, State
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from holla import makeHolla
from two_tangs import makeTangs


dataframe = None


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
        pylayout.HTML_ROW_TABLE,
        pylayout.HTML_ROW_BUTTON_VIZ,
        pylayout.HTML_ROW_GRAPH_ONE,
    ],
    fluid=True,
    className="dbc",
)

@app.callback(
    [
        Output("row-table-uploaded", "children"),
        Output("button-visualize", "disabled"),
        Output("button-visualize", "outline"),
    ],
    Input("dcc-upload", "contents"),
    State("dcc-upload", "filename"),
    State("dcc-upload", "last_modified"),
    Input("button-skip", "n_clicks"),
    prevent_initial_call=True,
)
def callback_upload(content, filename, filedate, _):
    ctx = dash.callback_context

    global dataframe

    if content is not None:
        children, dataframe = pyfunc.parse_upload_data(content, filename, filedate)

    if ctx.triggered[0]["prop_id"] == "button-skip.n_clicks":
        dataframe = pd.read_csv(
            Path(r"./inj_well_36.csv"), index_col=0, parse_dates=True,
            usecols=["date", "Qприем ТМ", "Рбуф", "Dшт"]
        )
        filename = None
        filedate = None

    button_viz_disabled = True
    button_viz_outline = True

    if dataframe is not None:
        editable = [False] + [True] * len(dataframe.columns)
        children = pylayoutfunc.create_table_layout(
            dataframe,
            "output-table",
            filename=filename,
            filedate=filedate,
            editable=editable,
            renamable=True,
        )
        button_viz_disabled = False
        button_viz_outline = False

    return [
        children,
        button_viz_disabled,
        button_viz_outline,
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
