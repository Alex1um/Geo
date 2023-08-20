import pandas as pd
from dash import Output, Input, State, ctx

from components.main_table_config_modal.markup import CONFIG_MODAL, BT_CANCEL, BT_OK, COL_P, COL_Q, COL_DATE, COL_ND, \
    PREVIEW_TABLE, TABLE_START_ROW, COL_DATE_TYPE, COL_P0, TABLE_START_COL
from components.main_page.markup import MAIN_COMPONENT, UPLOAD_COMPONENT, REASSIGN_BUTTON
from components.memory import SOURCE_TABLE, MAIN_TABLE_CONFIG
from dash_app import app
from typing import Union, Literal
from components.hall_tab import START_BUTTON as HALL_START_BUTTON
from tools import make_columns_unique


@app.callback(
    [
        Output(TABLE_START_ROW, "value"),
    ],
    [
        Input(BT_CANCEL, "n_clicks"),
    ],
    State(MAIN_TABLE_CONFIG, "data"),
    prevent_initial_call=True,
)
def on_cancel(_, current_config: dict):
    if current_config:
        return [
            current_config["start_row"],
        ]
    else:
        return [
            0,
        ]


@app.callback(
    [
        Output(MAIN_TABLE_CONFIG, "data"),
    ],
    Input(BT_OK, "n_clicks"),
    [
        State(TABLE_START_ROW, "value"),
        State(TABLE_START_COL, "value"),
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
    start_col: int,
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
        "start_col": start_col,
        "cols_date": date_colls_names,
        "date_type": date_col_type,
    }
    return [
        data,
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
        Output(COL_DATE, "value"),
        Output(COL_Q, "value"),
        Output(COL_P, "value"),
        Output(COL_ND, "value"),
        Output(COL_P0, "value"),
    ],
    [
        Input(TABLE_START_ROW, "value"),
        Input(TABLE_START_COL, "value"),
        Input(SOURCE_TABLE, "data"),
    ],
    [
        State(TABLE_START_ROW, "value"),
        State(PREVIEW_TABLE, "data"),
        State(MAIN_TABLE_CONFIG, "data"),
    ],
    prevent_initial_call=True,
)
def on_start_change_or_init_on_source_data(
    new_start_row,
    new_start_col,
    all_data, 
    old_start,
    preview_data,
    current_config,
):

    dataframe_source = pd.DataFrame(all_data)
    data = []
    cols = []
    if new_start_row >= 0:
        new_dataframe = dataframe_source.iloc[new_start_row:new_start_row + 5, new_start_col:]
        if new_start_row == 0:
            columns = dataframe_source.columns[new_start_col:]
        else:
            columns = dataframe_source.iloc[new_start_row - 1, new_start_col:]
        new_dataframe.columns = make_columns_unique(columns)
        cols = new_dataframe.columns.array
        data = new_dataframe.to_dict("records")
    if current_config and current_config["start_row"] == new_start_row:
        return [
            data,
            cols,
            cols,
            cols,
            cols,
            cols,
            current_config["cols_date"],
            current_config["col_q"],
            current_config["col_p"],
            current_config.get("col_md", None),
            current_config.get("col_p0", None),
        ]
    else:
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
    Output(CONFIG_MODAL, "is_open"),
    [
        Input(HALL_START_BUTTON, "n_clicks"),
        Input(REASSIGN_BUTTON, "n_clicks"),
        Input(SOURCE_TABLE, "data"),
        Input(BT_OK, "n_clicks"),
        Input(BT_CANCEL, "n_clicks"),
    ],
    State(COL_P0, "value"),
    prevent_initial_call=True,
)
def modal_open_close_triggers(
    hall_start_clicks, 
    reassign_clicks,
    source_data,
    ok_clicks,
    cancel_clicks,
    p0_val
):
    if ctx.triggered_id in {REASSIGN_BUTTON.id, SOURCE_TABLE.id}:
        return True
    elif ctx.triggered_id == HALL_START_BUTTON.id and p0_val is None:
        return True
    else:
        return False


@app.callback(
    Output(COL_DATE_TYPE, "disabled"),
    Input(COL_DATE, "value"),
    prevent_initial_call=True,
)
def on_type_change(
    date_cols: list[str],
):
    return bool(date_cols) and len(date_cols) > 1
# Union[Literal['auto'], Literal['s'], Literal['h'], Literal['D'], Literal['M'], Literal['Y']]


@app.callback(
    [
        Output(COL_P0, "className"),
    ],
    [
        Input(HALL_START_BUTTON, "n_clicks"),
        Input(COL_P0, "value"),
    ],
    [
        State(COL_P0, "className"),
        State(CONFIG_MODAL, "is_open"),
    ],
    prevent_initial_call=True,
)
def on_invalid_hall_start_and_edit(n_clicks, current_value, current_classes: str, is_opened):
    if current_value and "is-invalid" in current_classes:
        current_classes.removesuffix(" is-invalid")
    elif ctx.triggered_id == HALL_START_BUTTON.id:
        current_classes += " is-invalid"
    return [
        current_classes,
    ]
