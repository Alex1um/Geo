from dash import html, dcc
import dash_bootstrap_components as dbc
import pyfigure

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

HTML_ROW_TABLE = html.Div(
    dbc.Container(
        [
            dbc.Card(
                dbc.CardBody(
                    id="row-table-uploaded",
                    children=dcc.Graph(
                        figure=pyfigure.figure_empty(),
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
                            dbc.Button(
                                "Download Table as CSV",
                                color="primary",
                                className="fs-4",
                                id="button-download-csv",
                            ),
                            dcc.Download(id="download-csv"),
                        ],
                        width="auto",
                        style={"visibility": "hidden"},
                        id="row-button-download-csv",
                    ),
                    dbc.Col(
                        [
                            dbc.Select(
                                options=["SRT", "Hall"],
                                value="Hall",
                                id="graph-selector",
                                # className="form-select"
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

HTML_ROW_OPTIONS_GRAPH_RAINFALL = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label("Small Dataset (<= 2,920 data points) Options:"),
                            dbc.RadioItems(
                                options=[
                                    {"label": "Stack", "value": "stack"},
                                    {"label": "Group", "value": "group"},
                                    {"label": "Line", "value": "line"},
                                ],
                                value="stack",
                                id="radio-graphbar-options",
                                inline=True,
                            ),
                        ],
                        width="auto",
                    )
                ],
                justify="center",
            )
        ],
        fluid=True,
        style={"visibility": "hidden"},
        id="container-graphbar-options",
    )
)

HTML_ROW_GRAPH_ONE = html.Div(
    dbc.Container(
        [
            dcc.Loading(
                dcc.Graph(
                    id="graph-rainfall",
                    figure=pyfigure.figure_empty(),
                    config={"staticPlot": True},
                )
            )
        ],
        fluid=True,
    )
)
