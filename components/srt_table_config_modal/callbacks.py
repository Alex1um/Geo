import pandas as pd
from dash import Output, Input, State, ctx

from components.srt_table_config_modal import CONFIG_MODAL, BT_CANCEL, BT_OK, COL_P, COL_Q, COL_DATE, \
    PREVIEW_TABLE, TABLE_START, COL_DATE_TYPE
from components.memory import SRT_TABLE, SRT_TABLE_CONFIG
from dash_app import app
from typing import Union, Literal


@app.callback(
    [
        Output(CONFIG_MODAL, "is_open", allow_duplicate=True),
        Output(TABLE_START, "value"),
    ],
    [
        Input(BT_CANCEL, "n_clicks"),
    ],
    State(SRT_TABLE_CONFIG, "data"),
    prevent_initial_call=True,
)
def on_cancel(_, current_config: dict):
    ...
    if current_config:
        return [
            False,
            current_config["start_row"],
        ]
    else:
        return [
            False,
            0,
        ]


@app.callback(
    [
        Output(SRT_TABLE_CONFIG, "data"),
        Output(CONFIG_MODAL, "is_open", allow_duplicate=True),
    ],
    Input(BT_OK, "n_clicks"),
    [
        State(TABLE_START, "value"),
        State(COL_DATE, "value"),
        State(COL_DATE_TYPE, "value"),
        State(COL_Q, "value"),
        State(COL_P, "value"),
    ],
    prevent_initial_call=True,
)
def on_ok(
    _,
    start_row: int,
    date_colls_names: list[str],
    date_col_type: Union[Literal["Date"], Literal["Time"]],
    col_q: str,
    col_p: str,
):
    data = {
        "col_q": col_q,
        "col_p": col_p,
        "start_row": start_row,
        "cols_date": date_colls_names,
        "date_type": date_col_type,
    }
    return [
        data,
        False,
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
    ],
    prevent_initial_call=True,
)
def check_ok(col_p_val, col_q_val, col_date_val):
    is_ready = not (col_p_val and col_q_val and col_date_val)
    return [
        is_ready,
        is_ready,
    ]


@app.callback(
    [
        Output(PREVIEW_TABLE, "data"),
        Output(COL_DATE, "options"),
        Output(COL_Q, "options"),
        Output(COL_P, "options"),
        Output(COL_DATE, "value", allow_duplicate=True),
        Output(COL_Q, "value", allow_duplicate=True),
        Output(COL_P, "value", allow_duplicate=True),
    ],
    [
        Input(TABLE_START, "value"),
        Input(SRT_TABLE, "data"),
    ],
    [
        State(TABLE_START, "value"),
        State(PREVIEW_TABLE, "data"),
        State(SRT_TABLE_CONFIG, "data"),
    ],
    prevent_initial_call=True,
)
def on_start_change_or_init_on_source_data(
    new_start,
    all_data, 
    old_start,
    preview_data,
    current_config,
):
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
    if current_config and current_config["start_row"] == new_start:
        return [
            data,
            cols,
            cols,
            cols,
            current_config["cols_date"],
            current_config["col_q"],
            current_config["col_p"],
        ]
    else:
        return [
            data,
            cols,
            cols,
            cols,
            None,
            None,
            None,
        ]


from components.srt_tab import SRT_REASSIGN


@app.callback(
    [
        Output(CONFIG_MODAL, "is_open", allow_duplicate=True),
    ],
    [
        Input(SRT_REASSIGN, "n_clicks"),
        Input(SRT_TABLE, "data"),
    ],
    prevent_initial_call=True,
)
def modal_open_triggers(bt_n_clicks: int, source_data):
    return [
        True
    ]


@app.callback(
    Output(COL_DATE_TYPE, "disabled"),
    Input(COL_DATE, "value"),
    prevent_initial_call=True,
)
def on_type_change(
    date_cols: list[str],
):
    return date_cols and len(date_cols) > 1
