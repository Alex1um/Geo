from dash import dash_table
from dash import dcc, html
from dash_app import app
import dash_bootstrap_components as dbc


CDF_CONTENT = dbc.CardGroup(
    [
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("xf"),
                                        PARAM_XF := dbc.Input(type="number")
                                    ],
                                    style={'width': "30%"},
                                ),
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("m"),
                                        PARAM_M := dbc.Input(type="number")
                                    ],
                                    style={'width': "30%"},
                                ),
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("h"),
                                        PARAM_H := dbc.Input(type="number")
                                    ],
                                    style={'width': "30%"},
                                ),
                            ],
                        ),
                        dbc.Row(
                            [
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("k"),
                                        PARAM_K := dbc.Input(type="number")
                                    ],
                                    style={'width': "30%"},
                                ),
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("S"),
                                        PARAM_S := dbc.Input(type="number")
                                    ],
                                    style={'width': "30%"},
                                ),
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("Cs"),
                                        PARAM_CS := dbc.Input(type="number")
                                    ],
                                    style={'width': "30%"},
                                ),
                            ],
                        ),
                        dbc.Row(
                            [
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("KfWf"),
                                        PARAM_KFWF := dbc.Input(type="number")
                                    ],
                                    className="g-col-1",
                                    style={'width': "30%"},
                                ),
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("Pi"),
                                        PARAM_PI := dbc.Input(type="number")
                                    ],
                                    className="g-col-1",
                                    style={'width': "30%"},
                                ),
                            ],
                        ),
                    ],
                    className="d-flex flex-column row-gap-3"
                ),
                dbc.CardFooter(
                    [
                        PROCESS_BUTTON := dbc.Button(
                            "Process",
                            outline=True,
                            disabled=True,
                        ),
                    ],
                ),
            ]
        ),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dcc.Loading(
                            [
                                MAIN_GRAPH := dcc.Graph(id='cdf-graph')
                            ]
                        )
                    ]
                )
            ]
        ),
    ],
    className="d-none flex-column gap-3 mt-3",
) 


CDF_TAB = html.Div(
    [
        START_COMPONENT := dbc.Container(
            [
                START_BUTTON := dbc.Button(
                    [
                        "start",
                    ],
                    id="cdf-start",
                )
            ],
            className="d-flex justify-content-center align-items-center",
            style={"height": "25vh"},
        ),
        CDF_CONTENT
    ]
)
