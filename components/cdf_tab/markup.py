from dash import dash_table
from dash import dcc, html
from dash_app import app
import dash_bootstrap_components as dbc


CDF_CONTENT = dbc.CardGroup(
    [
        dbc.Card(
            [
                dbc.InputGroup(
                    [
                        PARAM_XF := dbc.Input(type="number")
                    ]
                ),
                dbc.InputGroup(
                    [
                        PARAM_M := dbc.Input(type="number")
                    ]
                ),
                dbc.InputGroup(
                    [
                        PARAM_H := dbc.Input(type="number")
                    ]
                ),
                dbc.InputGroup(
                    [
                        PARAM_K := dbc.Input(type="number")
                    ]
                ),
                dbc.InputGroup(
                    [
                        PARAM_S := dbc.Input(type="number")
                    ]
                ),
                dbc.InputGroup(
                    [
                        PARAM_CS := dbc.Input(type="number")
                    ]
                ),
                dbc.InputGroup(
                    [
                        PARAM_KW := dbc.Input(type="number")
                    ]
                ),
                dbc.InputGroup(
                    [
                        PARAM_PI := dbc.Input(type="number")
                    ]
                ),
            ]
        ),
        dbc.Card(
            [
                MAIN_GRAPH := dcc.Graph(id='cdf')
            ]
        ),
    ],
    className="d-none flex-column gap-3",
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
