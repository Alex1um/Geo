from dash_app import app
from components.cdf_tab import *
from dash import Input, Output, State
from components.main_page import MAIN_TABLE as DATA_TABLE
import pandas as pd
import plotly.graph_objects as go


@app.callback(
    [
        Output(START_COMPONENT, "className"),
        Output(CDF_CONTENT, "className"),
    ],
    [
        Input(START_BUTTON, "n_clicks"),
    ],
    [
        State(START_COMPONENT, "className"),
        State(CDF_CONTENT, "className"),
    ],
    prevent_initial_call=True,
)
def on_start_click(_, class_start, class_cdf_cont):
    return [
        class_start.replace("d-flex", "d-none"),
        class_cdf_cont.replace("d-none", "d-flex"),
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


app.callback(
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
    cs,
    h,
    k,
    kfwf,
    m,
    pi,
    s,
    xf,
    data
):

    dataframe = pd.DataFrame(data)
    dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime)
    dataframe = dataframe.set_index("DATE").sort_index()[["P", "Q", "P_0"]]

    return [
        go.Figure([])
    ]
