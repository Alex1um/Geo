from dash_app import app
from components.cdf_tab import *
from dash import Input, Output, State
from components.main_page import MAIN_PLOT as DATA_PLOT
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
    
app.callback(
    [
        Output(MAIN_GRAPH, "figure"),
    ],
    [
        Input(PARAM_CS, "value"),
        Input(PARAM_H, "value"),
        Input(PARAM_K, "value"),
        Input(PARAM_KW, "value"),
        Input(PARAM_M, "value"),
        Input(PARAM_PI, "value"),
        Input(PARAM_S, "value"),
        Input(PARAM_XF, "value"),
    ],
    State(DATA_PLOT, "derived_virtual_data")
)
def on_all_params(
    cs,
    h,
    k,
    kw,
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
        go.Figure()
    ]
