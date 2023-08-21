from dash import dash_table
from dash import dcc, html
from dash_app import app
import dash_bootstrap_components as dbc

HALL_PLOTS = dbc.CardGroup(
    [
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dcc.Loading(
                            [
                                RANGE_GRAPH := dcc.Graph(
                                    id="hall-range-plot",
                                )
                            ]
                        )
                    ],
                ),
            ],
        ),
        HALL_PROCESS_BT := dbc.Button(
            html.P(
                "Transform",
                style={"transform": "rotate(90deg)"}),
                id="hall-process",
            ),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dcc.Loading(
                            [
                                HALL_GRAPH := dcc.Graph(
                                    id="hall-graph"
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ],
    className="d-none gap-2 mt-3"
)

HALL_TAB = html.Div(
    [
        START_COMPONENT := dbc.Container(
            [
                START_BUTTON := dbc.Button(
                    [
                        "start",
                    ],
                    id="hall-start",
                )
            ],
            className="d-flex justify-content-center align-items-center",
            style={"height": "25vh"},
        ),
        HALL_PLOTS
    ]
)
