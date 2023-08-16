from dash import dash_table
from dash import html, dcc
import dash_bootstrap_components as dbc
from empty import figure_empty

HTML_TITLE = html.Div(
    [
        html.H1(
            "asd",
            className="float fw-bold text-center mt-3 fs-1 fw-bold",
        ),
    ],
    className="text-center",
)

DCC_UPLOAD = html.Div(
    dcc.Upload(
        id="dcc-upload",
        children=html.Div(
            [
                dbc.Button(
                    "Drag and Drop or Select Files",
                    color="primary",
                    outline=False,
                    class_name="fs-4 text-center",
                    id="button-upload",
                )
            ]
        ),
        multiple=False,
        disable_click=False,
    ),
)

HTML_ROW_BUTTON_UPLOAD = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [DCC_UPLOAD],
                        width="auto",
                    ),
                    dbc.Col(
                        [
                            dbc.Button(
                                "Use Example Data",
                                color="info",
                                id="button-skip",
                                class_name="fs-4 text-center",
                            ),
                        ],
                        class_name="fs-4 text-center",
                        width="auto",
                    ),
                ],
                justify="center",
            ),
        ],
        fluid=True,
    ),
)

TABLE_BEGIN = dbc.Container(
    [
        dbc.Row(
            [dbc.Col(dbc.Input(type="number", id="select-start", value=0))],
        ),
        dbc.Row(
            [
                dbc.Col(dash_table.DataTable(
                    id="table-begin-table",
                    style_table={"overflowX": "auto"},
                    page_size=10,
                ))
            ]
        ),
        dbc.Row(
            [
                dbc.Col("Date fields"),
                dbc.Col("Q"),
                dbc.Col("P"),
                dbc.Col("Р_0")
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(id="select-date", multi=True)),
                dbc.Col(dcc.Dropdown(id="select-q")),
                dbc.Col(dcc.Dropdown(id="select-p")),
                dbc.Col(dcc.Dropdown(id="select-p0")),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Button(["Submit"], id="table-begin-submit", disabled=True)),
            ]
        )
    ],
    id="table-begin",
    fluid=True,
    style={"visibility": "hidden"},
)

HTML_ROW_TABLE = html.Div(
    dbc.Container(
        [
            dbc.Card(
                dbc.CardBody(
                    id="row-table-uploaded",
                    children=dcc.Graph(
                        figure=figure_empty(),
                        config={"staticPlot": True},
                    ),
                ),
            ),
        ],
        fluid=True,
        class_name="my-3",
    )
)

HTML_ROW_BUTTON_VIZ = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            "Visualize Data",
                            color="success",
                            outline=True,
                            class_name="fs-4 fw-bold",
                            id="button-visualize",
                            disabled=True,
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                options=["SRT", "Hall"],
                                value="Hall",
                                id="graph-selector",
                            )
                        ]
                    )
                ],
                justify="center",
            )
        ],
        class_name="my-4",
    )
)

HTML_ROW_GRAPH_ONE = html.Div(
    dbc.Container(
        [
            dcc.Loading(
                dcc.Graph(
                    id="graph-rainfall",
                    figure=figure_empty(),
                    config={"staticPlot": True},

                ),
            )
        ],
        fluid=True,
        id="graph-container"
    )
)
