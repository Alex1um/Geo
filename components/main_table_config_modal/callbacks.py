import pandas as pd
from dash import Output, Input, State

from components.main_table_config_modal.markup import CONFIG_MODAL, BT_CANCEL, BT_OK, COL_P, COL_Q, COL_DATE, COL_ND, \
    TABLE_PREVIEW, TABLE_START
from components.main_page.markup import MAIN_TABLE, MAIN_COMPONENT, UPLOAD_COMPONENT
from dash_app import app
import io
import base64


@app.callback(
    [
        Output(CONFIG_MODAL, "is_open"),
        Output(TABLE_START, "value"),
    ],
    [
        Input(MAIN_TABLE, "data"),
    ],
    prevent_initial_call=True,
)
def on_data_upload(_):
    return [
        True,
        0
    ]


@app.callback(
    [
        Output(CONFIG_MODAL, "is_open", allow_duplicate=True),
    ],
    [
        Input(BT_CANCEL, "n_clicks"),
        Input(BT_OK, "n_clicks"),
    ],
    prevent_initial_call=True,
)
def callback_to_close_modal(cancel_n: int, ok_n: int):
    ...
    return [
        False
    ]


@app.callback(
    [
        Output(BT_OK, "disabled"),
        Output(BT_OK, "outline"),
    ],
    [
        Input(COL_P, "value"),
        Input(COL_Q, "value"),
        Input(COL_DATE, "value"),
        Input(COL_ND, "value"),
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
        Output(TABLE_PREVIEW, "data"),
        Output(COL_DATE, "options"),
        Output(COL_Q, "options"),
        Output(COL_P, "options"),
        Output(COL_ND, "options"),
        Output(COL_DATE, "value"),
        Output(COL_Q, "value"),
        Output(COL_P, "value"),
        Output(COL_ND, "value"),
    ],
    Input(TABLE_START, "value"),
    State(TABLE_START, "value"),
    State(MAIN_TABLE, "derived_virtual_data"),
    State(TABLE_PREVIEW, "data"),
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
