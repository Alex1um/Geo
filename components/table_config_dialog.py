from dash import dash_table
from dash import html, dcc, Input, Output, State
from dash_app import app
import dash_bootstrap_components as dbc
import pandas as pd
from components.main import MAIN_TABLE, MAIN_CONTENT


UPLOAD_MODAL_CONTENT = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        table_start := dbc.Input(type="number", id="upload-modal-select-start", value=0),
                    ],
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        table_preview := dash_table.DataTable(
                            id="upload-modal-table",
                            style_table={"overflowX": "auto"},
                            page_size=10,
                        ),
                    ],
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col("Date fields"),
                dbc.Col("Q"),
                dbc.Col("P"),
                dbc.Col("Р_0")
            ],
            className="mt-2",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                col_date := dcc.Dropdown(id="select-date", multi=True),
                            ]
                        ),
                        dbc.Row(
                            [
                                col_date_type := dcc.RadioItems(
                                    id="select-date-type",
                                    options=["Time", "Date"],
                                    value="Date",
                                    className="form-check",
                                    inputClassName="form-check-input",
                                    labelClassName="form-check-label"
                                )
                            ]
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        col_q := dcc.Dropdown(id="select-q"),
                    ],
                ),
                dbc.Col(
                    [
                        col_p := dcc.Dropdown(id="select-p")
                    ],
                ),
                dbc.Col(
                    [
                        col_nd := dcc.Dropdown(id="select-nozzle-diameter"),
                    ],
                ),
            ]
        ),
    ],
    id="table-begin",
    className="gap-2",
    fluid=True,
)

UPLOAD_MODAL = dbc.Modal(
    [
        dbc.ModalHeader(
            [
                dbc.ModalTitle(
                    "Configure Table",
                ),
            ],
            close_button=False,
        ),
        dbc.ModalBody(
            children=UPLOAD_MODAL_CONTENT,

        ),
        dbc.ModalFooter(
            [
                bt_cancel := dbc.Button(
                    "Cancel",
                    color="secondary",
                    id="upload-modal-bt-cancel",
                ),
                bt_ok := dbc.Button(
                    "OK",
                    color="primary",
                    outline=True,
                    id="upload-modal-bt-ok",
                    disabled=True,
                )
            ]
        )
    ],
    id="modal-table-config",
    size="xl",

)


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


