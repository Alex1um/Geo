from components.srt_tab import *
from components.main_page import MAIN_TABLE
from dash_app import app
from dash import Input, Output, State, dcc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from two_tangs import makeTangs


@app.callback(
    [
        Output(START_COMPONENT, "className"),
        Output(SRT_PLOTS, "className"),
        Output(CHOOSE_GRAPH, "figure", allow_duplicate=True),
        Output(SRT_GRAPH, "figure", allow_duplicate=True),
    ],
    [
        Input(START_BUTTON, "n_clicks"),
    ],
    [
        State(MAIN_TABLE, "derived_virtual_data"),
        State(START_COMPONENT, "className"),
        State(SRT_PLOTS, "className"),
    ],
    prevent_initial_call=True,
)
def on_start(_, data, class_start: str, class_hall: str):

    dataframe = pd.DataFrame(data)
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
        class_start.replace("d-flex", "d-none"),
        class_hall.replace("d-none", "d-flex"),
        main_fig,
        fig,
    ]


@app.callback(
    [
        Output(CHOOSE_GRAPH, "figure", allow_duplicate=True),
        Output(SRT_GRAPH, "figure", allow_duplicate=True),
    ],
    [
        Input(CHOOSE_GRAPH, "clickData"),
    ],
    [
        State(CHOOSE_GRAPH, "figure"),
        State(SRT_GRAPH, "figure")
    ],
    prevent_initial_call=True,
)
def on_graph_click(clickData, fig: dict, regr_fig: dict):
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

    return fig, regr_fig

