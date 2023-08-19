from components.srt_tab import *
from dash_app import app
from dash import Input, Output, State, dcc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from two_tangs import makeTangs
from components.memory import SRT_TABLE, SRT_TABLE_CONFIG, MAIN_TABLE_CONFIG, SOURCE_TABLE
import base64
import io



@app.callback(
    [
        Output(SRT_TABLE, "data", allow_duplicate=True),
        Output(SRT_TABLE_CONFIG, "data", allow_duplicate=True),
        Output(START_COMPONENT, "className"),
        Output(SRT_PLOTS, "className"),
    ],
    [
        Input(START_BUTTON, "n_clicks")
    ],
    [
        State(SOURCE_TABLE, "data"),
        State(MAIN_TABLE_CONFIG, "data"),
        State(START_COMPONENT, "className"),
        State(SRT_PLOTS, "className"),
    ],
    prevent_initial_call=True,
)
def on_start_button(_, src_table, src_config, class_start: str, class_srt: str):
    return [
        src_table,
        src_config,
        class_start.replace("d-flex", "d-none"),
        class_srt.replace("d-none", "d-flex"),
    ]


@app.callback(
    [
        Output(CHOOSE_GRAPH, "figure", allow_duplicate=True),
        Output(SRT_GRAPH, "figure", allow_duplicate=True),
    ],
    [
        Input(SRT_TABLE_CONFIG, "data"),
    ],
    [
        State(SRT_TABLE, "data"),
    ],
    prevent_initial_call=True,
)
def on_setup(table_config, main_table_data):

    if not main_table_data or not table_config:
        return [
            go.Figure(), go.Figure()
        ]

    start_row: int = table_config["start_row"]
    date_colls_names: list[str] | str = table_config["cols_date"]
    date_col_type = table_config["date_type"]
    q_col: str = table_config["col_q"]
    p_col: str = table_config["col_p"]
    
    dataframe = pd.DataFrame(main_table_data)
    if start_row > 0:
        dataframe.columns = dataframe.iloc[start_row - 1]
    else:
        dataframe.columns = dataframe.columns
    dataframe = dataframe.iloc[start_row:]
    
    cols = list(filter(bool, [*date_colls_names, q_col, p_col]))
    dataframe = dataframe[cols]
    if len(date_colls_names) > 1:
        dataframe["DATE"] = dataframe[date_colls_names].apply(lambda x: ' '.join(x.astype(str)), axis=1)
        dataframe.drop(date_colls_names, axis=1, inplace=True)
        dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime)
        # dataframe = dataframe.set_index("DATE").sort_index()
    else:
        # dataframe["DATE"] = dataframe[date_colls_names].apply(lambda x: ' '.join(x.astype(str)), axis=1)
        dataframe = dataframe.rename(columns={date_colls_names[0]: "DATE"})
        if date_col_type != "auto":
            dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime, unit=date_col_type)
        else:
            dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime)

        # dataframe = dataframe.set_index(date_colls_names).sort_index()
    dataframe = dataframe.rename(columns={q_col: "Q", p_col: "P"})

    # dataframe = pd.DataFrame(data)
    dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime)
    dataframe = dataframe.set_index("DATE").sort_index()

    main_fig = make_subplots(specs=[[{"secondary_y": True}]])

    main_fig.add_trace(
        go.Scatter(x=dataframe.index, y=dataframe["P"], name="Pressure"),
        secondary_y=False,
    )
    main_fig.add_trace(
        go.Scatter(x=dataframe.index, y=dataframe['Q'], name="Flow Rate", opacity=0.5),
        secondary_y=True,
    )

    main_fig.update_layout(
        title_text="<b>Select the points</b>",
        xaxis=dict(
            title="<b>Time</b>"
        ),
        yaxis=dict(
            title="<b>Pressure</b>",
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),
        yaxis2=dict(
            title="Flow Rate",
            titlefont=dict(
                color="#ff7f0e"
            ),
            tickfont=dict(
                color="#ff7f0e"
            )
        ),
    )
    selected_points = go.Scatter(x=[], y=[], mode="markers", name="Selected Points",
                                    marker={"color": "#000000", "size": 10, "symbol": "x-thin", "line": {"width": 2}})
    main_fig.add_trace(
        selected_points,
        secondary_y=False,
    )

    grph = dcc.Graph(figure=main_fig)


    layout_regression = go.Layout(hovermode="closest",
                                    title="<b>SRTest</b>",
                                    yaxis={"title": "<b>Pressure<b>"},
                                    xaxis={"title": "<b>Flow Rate</b>"},
                                    legend={"title": "Legend"})

    regr_left = go.Scatter(x=[], y=[], mode="lines", name="Left Regression")
    regr_right = go.Scatter(x=[], y=[], mode="lines", name="Right Regression")
    cross_point = go.Scatter(x=[], y=[], mode="markers+text", name="Fracturing Pressure",
                                marker={"color": "#ff0000", "size": 10, "symbol": "circle", "line": {"width": 2}},
                                text="P frac", textposition='top left', textfont={'size': 14})
    fig = go.Figure([selected_points, regr_left, regr_right, cross_point], layout_regression)
    
    return [
        main_fig,
        fig,
    ]


@app.callback(
    [
        Output(CHOOSE_GRAPH, "figure", allow_duplicate=True),
        Output(SRT_GRAPH, "figure", allow_duplicate=True),
        Output(P_FRAC, "value"),
    ],
    [
        Input(CHOOSE_GRAPH, "clickData"),
    ],
    [
        State(P_FRAC, "value"),
        State(CHOOSE_GRAPH, "figure"),
        State(SRT_GRAPH, "figure")
    ],
    prevent_initial_call=True,
)
def on_graph_click(clickData, p_frac: float, fig: dict, regr_fig: dict):
    curves = len(fig['data'])
    if clickData:
        new_x, new_y = clickData['points'][0]['x'], clickData['points'][0]['y']
        y: list = fig['data'][-1]['y']
        x: list = fig['data'][-1]['x']
        if clickData['points'][0]['curveNumber'] == 0:
            y.append(new_y)
            x.append(new_x)
        elif clickData['points'][0]['curveNumber'] == curves - 1:
            i = x.index(new_x)
            x.pop(i)
            y.pop(i)

        regr_fig['data'][0]['x'] = x
        regr_fig['data'][0]['y'] = y

        print("y = ", y, type(y))
        print('x = ', x, type(x))

        if len(x) >= 4:
            y_left, y_right, cross = makeTangs(x, y)

            # regr_fig['layout']['text'] = f'''
            # Fracturing Pressure = {cross[0] / 1000000} МПа
            # '''

            # m, c = np.linalg.lstsq(A, np.array(y), rcond=None)[0]
            regr_fig['data'][1]['x'] = x
            regr_fig['data'][1]['y'] = y_left

            regr_fig['data'][2]['x'] = x
            regr_fig['data'][2]['y'] = y_right

            regr_fig['data'][3]['x'] = [cross[0]]
            regr_fig['data'][3]['y'] = [cross[1]]

            p_frac = cross[1]

    return fig, regr_fig, p_frac




@app.callback(
    [
        Output(SRT_TABLE, "data"),
    ],
    Input(SRT_UPlOAD, "contents"),
    State(SRT_UPlOAD, "filename"),
    State(SRT_UPlOAD, "last_modified"),
    prevent_initial_call=True,
)
def on_srt_table_upload(content, filename, filedate):
    # global dataframe_source

    dataframe_source = None

    if content is not None:
        _, content_string = content.split(",")

        decoded = base64.b64decode(content_string)

        if filename.endswith(".csv"):
            dataframe_source = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            dataframe_source = pd.read_excel(decoded)

    return [
        dataframe_source.to_dict("records"),
    ]