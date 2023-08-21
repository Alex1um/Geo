
from dash import dash_table
from dash import dcc, html
from dash_app import app
import dash_bootstrap_components as dbc


SRT_PLOTS = dbc.CardGroup(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dbc.Label(
                                            "P frac"
                                        ),
                                        P_FRAC := dbc.Input(
                                            id="p-frac-input",
                                            type="number",
                                            value=0,
                                            step=0.01
                                        )
                                    ],
                                    className="center-text text-center"
                                )
                            ],
                            # className="d-inline",
                        ),
                    ],
                    className="d-flex justify-content-center",
                )
            ],
            className="container-fluid",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        SRT_UPlOAD := dcc.Upload(
                                            [
                                                dbc.Button(
                                                    "Upload SRT",
                                                    outline=False,
                                                    className="text-center",
                                                    id="srt-table-upload-button"
                                                )
                                            ]
                                        ),
                                        SRT_REASSIGN := dbc.Button(
                                            [
                                                "Edit uploaded table"
                                            ]
                                        )
                                    ],
                                    className="d-flex gap-3 justify-content-center"
                                )
                            ]
                        )
                    ],
                    className="d-flex justify-content-center",
                )
            ],
            className="container-fluid",
        ),
        dbc.Row(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                dcc.Loading(
                                    [
                                        CHOOSE_GRAPH := dcc.Graph(
                                            id="srt-choose-graph",
                                        )
                                    ]
                                )
                            ],
                        ),
                    ],
                    className="col",
                ),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                dcc.Loading(
                                    [
                                        SRT_GRAPH := dcc.Graph(
                                            id="srt-graph"
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    className="col",
                )
            ],
            className="gap-3 container-fluid"
        ),
    ],
    className="d-none gap-3 mx-2 mt-3"
)

SRT_TAB = html.Div(
    [
        START_COMPONENT := dbc.Container(
            [
                START_BUTTON := dbc.Button(
                    [
                        "start",
                    ],
                    id="srt-start",
                )
            ],
            className="d-flex justify-content-center align-items-center",
            style={"height": "25vh"},
        ),
        SRT_PLOTS
    ]
)
