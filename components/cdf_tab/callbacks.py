from dash_app import app
from components.cdf_tab import *
from dash import Input, Output, State, no_update
from components.main_page import MAIN_TABLE as DATA_TABLE
import pandas as pd
import plotly.graph_objects as go
from gdis_kpd import solve_kpd
from plotly.subplots import make_subplots
import numpy as np
from components.memory import GDIS_PARAMS


@app.callback(
    [
        Output(START_COMPONENT, "className"),
        Output(CDF_CONTENT, "className"),
        Output(PARAM_CS, "value"),
        Output(PARAM_H, "value"),
        Output(PARAM_K, "value"),
        Output(PARAM_KFWF, "value"),
        Output(PARAM_M, "value"),
        Output(PARAM_PI, "value"),
        Output(PARAM_S, "value"),
        Output(PARAM_XF, "value"),
    ],
    [
        Input(START_BUTTON, "n_clicks"),
    ],
    [
        State(START_COMPONENT, "className"),
        State(CDF_CONTENT, "className"),
        State(GDIS_PARAMS, "data"),
    ],
    prevent_initial_call=True,
)
def on_start_click(_, class_start, class_cdf_cont, gdis_params):

    if gdis_params:
        return [
            class_start.replace("d-flex", "d-none"),
            class_cdf_cont.replace("d-none", "d-flex"),
            *(gdis_params[param] for param in map(lambda x: x.id, (PARAM_H, PARAM_XF, PARAM_K, PARAM_M, PARAM_S, PARAM_CS, PARAM_PI, PARAM_KFWF)))
        ]

    return [
        class_start.replace("d-flex", "d-none"),
        class_cdf_cont.replace("d-none", "d-flex"),
        *[no_update] * 8
    ]


@app.callback(
    [
        Output(PROCESS_BUTTON, "disabled"),
        Output(PROCESS_BUTTON, "outline"),
    ],
    [
        Input(PARAM_CS, "value"),
        Input(PARAM_H, "value"),
        Input(PARAM_K, "value"),
        Input(PARAM_KFWF, "value"),
        Input(PARAM_M, "value"),
        Input(PARAM_PI, "value"),
        Input(PARAM_S, "value"),
        Input(PARAM_XF, "value"),
    ],
    prevent_initial_call=True,
)
def validate_inputs(
    cs,
    h,
    k,
    kfwf,
    m,
    pi,
    s,
    xf,
):
    disabled = not all((cs, h, k, kfwf, m, pi, s, xf))
    return disabled, disabled


@app.callback(
    [
        Output(MAIN_GRAPH, "figure"),
    ],
    [
        Input(PROCESS_BUTTON, "n_clicks"),
    ],
    [
        State(PARAM_CS, "value"),
        State(PARAM_H, "value"),
        State(PARAM_K, "value"),
        State(PARAM_KFWF, "value"),
        State(PARAM_M, "value"),
        State(PARAM_PI, "value"),
        State(PARAM_S, "value"),
        State(PARAM_XF, "value"),
        State(DATA_TABLE, "derived_virtual_data"),
    ],
    prevent_initial_call=True,
)
def on_all_params(
    _,
    Cs,
    h,
    k,
    kfwf,
    poro,
    Pi,
    S,
    xf,
    data
):

    dataframe = pd.DataFrame(data)
    dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime)
    dataframe = dataframe.set_index("DATE").sort_index()

    Qinput = dataframe["Q"]
    Tinput = dataframe.index

    N = 150

    # применение функции solve_kpd
    # pressure, time, deltaP, log_derP = solve_kpd(Tinput, Qinput, xf, poro, h, k, S, Cs, kfwf, Pi, N)
    pressure, time = solve_kpd(Tinput, Qinput, xf, poro, h, k, S, Cs, kfwf, Pi, N)

    # df = pd.read_excel("saphir2 (2).xlsx", sheet_name="Лист2")
    # Trealdata = pd.to_datetime(df['t'], unit='h')

    # --------------------------------------------------------------------------------

    fig = make_subplots(rows=2, cols=1,
                        row_heights=[0.7, 0.3])

    fig.add_trace(go.Scatter(x=Tinput, y=dataframe['P'], name='Real Data', mode='markers',
                             marker={'line' : {'color' : 'blue', 'width' : 1}, 'size' : 3, 'symbol' : 'x-thin'},
                             ),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=time, y=pressure, line_shape='spline', name='Solve Data'), row=1, col=1)
    fig.add_trace(go.Scatter(x=Tinput, y=Qinput, line_shape='hv', name='Flow Rate'), row=2, col=1)

    # fig = make_subplots(rows=2, cols=2,
    #                     specs=[[{}, {"rowspan": 2}],
    #                            [{}, None]],
    #                     row_heights=[0.7, 0.3],
    #                     column_widths=[0.6, 0.4])
    #
    # fig.add_trace(go.Scatter(x=Tinput, y=dataframe['P'], name='Real Data', mode='markers',
    #                          marker={'line' : {'color' : 'blue', 'width' : 1}, 'size' : 3, 'symbol' : 'x-thin'}),
    #               row=1, col=1)
    # fig.add_trace(go.Scatter(x=time, y=pressure, line_shape='spline', name='Num Data'), row=1, col=1)
    # fig.add_trace(go.Scatter(x=Tinput, y=Qinput, line_shape='hv', name='Flow Rate'), row=2, col=1)
    #
    # fig.add_trace(go.Scatter(x=np.array(Tinput, dtype=f"datetime64[h]").astype(np.int64), y=deltaP), row=1, col=2)
    # fig.add_trace(go.Scatter(x=np.array(Tinput, dtype=f"datetime64[h]").astype(np.int64), y=log_derP), row=1, col=2)
    #
    # fig.update_xaxes(type="log", row=1, col=2)
    # fig.update_yaxes(type="log", row=1, col=2)


    return [
        fig
    ]


@app.callback(
    [
        Output(GDIS_PARAMS, "data")
    ],
    [
        Input(PROCESS_BUTTON, "n_clicks"),
    ],
    [
        State(PARAM_CS, "value"),
        State(PARAM_H, "value"),
        State(PARAM_K, "value"),
        State(PARAM_KFWF, "value"),
        State(PARAM_M, "value"),
        State(PARAM_PI, "value"),
        State(PARAM_S, "value"),
        State(PARAM_XF, "value"),
    ],
    prevent_initial_call=True,
)
def save_params(_, *params):
    return [{k:v for k, v in zip(map(lambda x: x.id, (PARAM_CS, PARAM_H, PARAM_K, PARAM_KFWF, PARAM_M, PARAM_PI, PARAM_S, PARAM_XF)), params)}]