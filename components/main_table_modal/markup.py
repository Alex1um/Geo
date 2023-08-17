from dash import dash_table
from dash import dcc, Output, State
from dash_app import app
import dash_bootstrap_components as dbc

_UPLOAD_MODAL_CONTENT = dbc.Container(
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
            children=_UPLOAD_MODAL_CONTENT,

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
