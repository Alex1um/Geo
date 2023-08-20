from dash import dash_table
from dash import dcc, html
from dash_app import app
import dash_bootstrap_components as dbc

_CONFIG_MODAL_CONTENT = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        TABLE_START_ROW := dbc.Input(type="number", id="upload-modal-select-start-row", value=0),
                    ],
                ),
                dbc.Col(
                    [
                        TABLE_START_COL := dbc.Input(type="number", id="upload-modal-select-start-col", value=0),
                    ],
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        PREVIEW_TABLE := dash_table.DataTable(
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
                dbc.Col("Nozzle diameter"),
                dbc.Col("P_0"),
            ],
            className="mt-2",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                COL_DATE := dcc.Dropdown(id="select-date", multi=True),
                            ]
                        ),
                        dbc.Row(
                            [
                                COL_DATE_TYPE := dcc.Dropdown(
                                    id="select-date-type",
                                    options=["s", "auto", "h", "D", "M", "Y"],
                                    value="s",
                                    clearable=False,
                                )
                            ]
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        COL_Q := dcc.Dropdown(id="select-q"),
                    ],
                ),
                dbc.Col(
                    [
                        COL_P := dcc.Dropdown(id="select-p")
                    ],
                ),
                dbc.Col(
                    [
                        COL_ND := dcc.Dropdown(id="select-nozzle-diameter"),
                    ],
                ),
                dbc.Col(
                    [
                        COL_P0 := dcc.Dropdown(id="select-p0", className="form-control"),
                    ],
                    className="form-floating",
                ),
            ]
        ),
    ],
    id="table-begin",
    className="gap-2",
    fluid=True,
)

CONFIG_MODAL = dbc.Modal(
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
            children=_CONFIG_MODAL_CONTENT,

        ),
        dbc.ModalFooter(
            [
                BT_CANCEL := dbc.Button(
                    "Cancel",
                    color="secondary",
                    id="upload-modal-bt-cancel",
                ),
                BT_OK := dbc.Button(
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
