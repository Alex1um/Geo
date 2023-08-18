import pandas as pd
from dash import Output, Input, State

from components.main_table_config_modal.markup import CONFIG_MODAL, BT_CANCEL, BT_OK, COL_P, COL_Q, COL_DATE, COL_ND, \
    PREVIEW_TABLE, TABLE_START, TABLE_CONFIG, COL_DATE_TYPE, COL_P0
from components.main_page.markup import SOURCE_TABLE, MAIN_COMPONENT, UPLOAD_COMPONENT, REASSIGN_BUTTON
from dash_app import app
from typing import Union, Literal


@app.callback(
    [
        Output(CONFIG_MODAL, "is_open", allow_duplicate=True),
        Output(TABLE_START, "value"),
        Output(COL_DATE, "value"),
        Output(COL_DATE_TYPE, "value"),
        Output(COL_Q, "value", allow_duplicate=True),
        Output(COL_P, "value", allow_duplicate=True),
        Output(COL_ND, "value", allow_duplicate=True),
        Output(COL_P0, "value", allow_duplicate=True),
    ],
    [
        Input(BT_CANCEL, "n_clicks"),
    ],
    State(TABLE_CONFIG, "data"),
    prevent_initial_call=True,
)
def on_cancel(_, current_config: dict):
    ...
    if current_config:
        return [
            False,
            current_config["start_row"],
            current_config["cols_date"],
            current_config["date_type"],
            current_config["col_q"],
            current_config["col_p"],
            current_config.get("col_md", None),
            current_config.get("col_p0", None),
        ]
    else:
        return [
            False,
            0,
            None,
            "Date",
            None,
            None,
            None,
            None,
        ]


@app.callback(
    [
        Output(TABLE_CONFIG, "data"),
        Output(CONFIG_MODAL, "is_open", allow_duplicate=True),
    ],
    Input(BT_OK, "n_clicks"),
    [
        State(TABLE_START, "value"),
        State(COL_DATE, "value"),
        State(COL_DATE_TYPE, "value"),
        State(COL_Q, "value"),
        State(COL_P, "value"),
        State(COL_ND, "value"),
        State(COL_P0, "value"),
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
    nd_col: str | None,
    p0_col: str | None,
):
    data = {
        "col_q": col_q,
        "col_p": col_p,
        "col_nd": nd_col,
        "col_p0": p0_col,
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
        Output(COL_ND, "options"),
        Output(COL_P0, "options"),
        Output(COL_DATE, "value", allow_duplicate=True),
        Output(COL_Q, "value", allow_duplicate=True),
        Output(COL_P, "value", allow_duplicate=True),
        Output(COL_ND, "value", allow_duplicate=True),
        Output(COL_P0, "value", allow_duplicate=True),
    ],
    [
        Input(TABLE_START, "value"),
        Input(SOURCE_TABLE, "data"),
    ],
    [
        State(TABLE_START, "value"),
        State(PREVIEW_TABLE, "data"),
    ],
    prevent_initial_call=True,
)
def on_start_change_or_init_on_source_data(
    new_start,
    all_data, 
    old_start,
    preview_data
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
    return [
        data,
        cols,
        cols,
        cols,
        cols,
        cols,
        None,
        None,
        None,
        None,
        None,
    ]


@app.callback(
    [
        Output(CONFIG_MODAL, "is_open", allow_duplicate=True),
    ],
    [
        Input(REASSIGN_BUTTON, "n_clicks"),
        Input(SOURCE_TABLE, "data"),
    ],
    prevent_initial_call=True,
)
def modal_open_callback(bt_n_clicks: int, source_data):
    return [
        True
    ]


@app.callback(
    [
        Output(COL_DATE, "multi"),
        Output(COL_DATE, "value", allow_duplicate=True),
    ],
    Input(COL_DATE_TYPE, "value"),
    State(COL_DATE, "value"),
    prevent_initial_call=True,
)
def on_type_change(
    date_col_type: Union[Literal["Date"], Literal["Time"]],
    current_value: list[str],
):
    multi = date_col_type == "Date"
    new_value = None
    if current_value:
        if multi:
            new_value = [current_value]
        else:
            new_value = current_value[0]
    return [
        multi,
        new_value
    ]
