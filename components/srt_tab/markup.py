
from dash import dash_table
from dash import dcc, html
from dash_app import app
import dash_bootstrap_components as dbc


SRT_PLOTS = dbc.CardGroup(
    [
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        CHOOSE_GRAPH := dcc.Graph(
                            id="srt-choose-graph",
                            )
                    ],
                ),
            ],
        ),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        SRT_GRAPH := dcc.Graph(
                            id="srt-graph"
                        )
                    ]
                )
            ]
        )
    ],
    className="d-none gap-2 mt-3"
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
