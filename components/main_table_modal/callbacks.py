import pandas as pd
from dash import Output, Input, State

from components.main_table_modal.markup import UPLOAD_MODAL, bt_cancel, bt_ok, col_p, col_q, col_date, col_nd, \
    table_preview, table_start
from components.main_page.markup import MAIN_TABLE, MAIN_CONTENT
from dash_app import app


@app.callback(
    [
        Output(UPLOAD_MODAL, "is_open", allow_duplicate=True),
    ],
    [
        Input(bt_cancel, "n_clicks"),
    ],
    prevent_initial_call=True,
)
def on_close(_):
    ...
    return [
        False
    ]


@app.callback(
    [
        Output(bt_ok, "disabled"),
        Output(bt_ok, "outline"),
    ],
    [
        Input(col_p, "value"),
        Input(col_q, "value"),
        Input(col_date, "value"),
        Input(col_nd, "value"),
    ],
    prevent_initial_call=True,
)
def check_ok(col_p_val, col_q_val, col_date_val, col_nd_val):
    is_ready = not (col_p_val and col_q_val and col_date_val)
    return [
        is_ready,
        is_ready,
    ]


@app.callback(
    [
        Output(table_preview, "data"),
        Output(col_date, "options"),
        Output(col_q, "options"),
        Output(col_p, "options"),
        Output(col_nd, "options"),
        Output(col_date, "value"),
        Output(col_q, "value"),
        Output(col_p, "value"),
        Output(col_nd, "value"),
    ],
    Input(table_start, "value"),
    State(table_start, "value"),
    State(MAIN_TABLE, "derived_virtual_data"),
    State(table_preview, "data"),
    prevent_initial_call=True,
)
def on_start_change(new_start, old_start, all_data, preview_data):
    dataframe_source = pd.DataFrame(all_data)
    data = []
    cols = []
    if new_start >= 0:
        new_dataframe = dataframe_source.iloc[new_start:new_start + 5]
        if new_start == 0:
            new_dataframe.columns = dataframe_source.columns
        else:
            new_dataframe.columns = dataframe_source.iloc[new_start - 1]
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
    Output(UPLOAD_MODAL, "is_open", allow_duplicate=True),
    Output(MAIN_CONTENT, "style"),
    [
        Input(bt_ok, "n_clicks"),
    ],
    prevent_initial_call=True,
)
def on_ok(_):

    return [
        False,
        {"display": "block"},
    ]
