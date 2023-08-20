import pandas as pd
from dash import Output, Input, State, ctx

from components.srt_table_config_modal import SRT_CONFIG_MODAL, SRT_BT_CANCEL, SRT_BT_OK, SRT_COL_P, SRT_COL_Q, SRT_COL_DATE, \
    SRT_PREVIEW_TABLE, SRT_TABLE_START, SRT_COL_DATE_TYPE
from components.memory import SRT_TABLE, SRT_TABLE_CONFIG
from dash_app import app
from typing import Union, Literal


@app.callback(
    [
        Output(SRT_TABLE_START, "value")
    ],
    [
        Input(SRT_BT_CANCEL, "n_clicks"),
        Input(SRT_TABLE_CONFIG, "data"),
    ],
    prevent_initial_call=True,
)
def srt_on_cancel(_, current_config: dict):
    if current_config:
        return current_config["start_row"],
    else:
        return 0,


@app.callback(
    [
        Output(SRT_TABLE_CONFIG, "data"),
    ],
    Input(SRT_BT_OK, "n_clicks"),
    [
        State(SRT_TABLE_START, "value"),
        State(SRT_COL_DATE, "value"),
        State(SRT_COL_DATE_TYPE, "value"),
        State(SRT_COL_Q, "value"),
        State(SRT_COL_P, "value"),
    ],
    prevent_initial_call=True,
)
def srt_on_ok(
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
    ]


@app.callback(
    [
        Output(SRT_BT_OK, "disabled"),
        Output(SRT_BT_OK, "outline"),
    ],
    [
        Input(SRT_COL_P, "value"),
        Input(SRT_COL_Q, "value"),
        Input(SRT_COL_DATE, "value"),
    ],
    prevent_initial_call=True,
)
def srt_check_ok(col_p_val, col_q_val, col_date_val):
    is_ready = not (col_p_val and col_q_val and col_date_val)
    return [
        is_ready,
        is_ready,
    ]


@app.callback(
    [
        Output(SRT_PREVIEW_TABLE, "data"),
        Output(SRT_COL_DATE, "options"),
        Output(SRT_COL_Q, "options"),
        Output(SRT_COL_P, "options"),
        Output(SRT_COL_DATE, "value"),
        Output(SRT_COL_Q, "value"),
        Output(SRT_COL_P, "value"),
    ],
    [
        Input(SRT_TABLE_START, "value"),
        Input(SRT_TABLE, "data"),
    ],
    [
        State(SRT_TABLE_START, "value"),
        State(SRT_PREVIEW_TABLE, "data"),
        State(SRT_TABLE_CONFIG, "data"),
    ],
    prevent_initial_call=True,
)
def srt_on_start_change_or_init_on_source_data(
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


from components.srt_tab import SRT_REASSIGN, SRT_UPlOAD


@app.callback(
    [
        Output(SRT_CONFIG_MODAL, "is_open")
    ],
    [
        Input(SRT_REASSIGN, "n_clicks"),
        Input(SRT_UPlOAD, "contents"),
        Input(SRT_BT_OK, "n_clicks"),
        Input(SRT_BT_CANCEL, "n_clicks"),
    ],
    prevent_initial_call=True,
)
def srt_modal_open_triggers(*_):
    if ctx.triggered_id in {SRT_REASSIGN.id, SRT_UPlOAD.id}:
        return True,
    else:
        return False,


@app.callback(
    Output(SRT_COL_DATE_TYPE, "disabled"),
    Input(SRT_COL_DATE, "value"),
    prevent_initial_call=True,
)
def srt_on_type_change(
    date_cols: list[str],
):
    return bool(date_cols) and len(date_cols) > 1
