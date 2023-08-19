from dash import dash_table
from dash import dcc, html
from dash_app import app
import dash_bootstrap_components as dbc

_SRT_CONFIG_MODAL_CONTENT = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        SRT_TABLE_START := dbc.Input(type="number", id="upload-srt-select-start", value=0),
                    ],
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        SRT_PREVIEW_TABLE := dash_table.DataTable(
                            id="upload-srt-table",
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
            ],
            className="mt-2",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                SRT_COL_DATE := dcc.Dropdown(id="select-srt-date", multi=True),
                            ]
                        ),
                        dbc.Row(
                            [
                                SRT_COL_DATE_TYPE := dcc.Dropdown(
                                    id="select-srt-date-type",
                                    options=["s", "auto", "h", "D", "M", "Y"],
                                    value="s",
                                    className="",
                                )
                            ]
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        SRT_COL_Q := dcc.Dropdown(id="select-srt-q"),
                    ],
                ),
                dbc.Col(
                    [
                        SRT_COL_P := dcc.Dropdown(id="select-srt-p")
                    ],
                ),
            ]
        ),
    ],
    id="srt-table-begin",
    className="gap-2",
    fluid=True,
)

SRT_CONFIG_MODAL = dbc.Modal(
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
            children=_SRT_CONFIG_MODAL_CONTENT,

        ),
        dbc.ModalFooter(
            [
                SRT_BT_CANCEL := dbc.Button(
                    "Cancel",
                    color="secondary",
                    id="upload-srt-modal-bt-cancel",
                ),
                SRT_BT_OK := dbc.Button(
                    "OK",
                    color="primary",
                    outline=True,
                    id="upload-srt-modal-bt-ok",
                    disabled=True,
                )
            ]
        )
    ],
    id="modal-srt-table-config",
    size="xl",

)
