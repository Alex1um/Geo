from dash import dash_table, html
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from components.hall_tab import HALL_TAB
from components.srt_tab import SRT_TAB
from components.cdf_tab import CDF_TAB
import plotly.graph_objects as go



MAIN_COMPONENT = dbc.CardGroup(
    [
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        MAIN_TABLE := dash_table.DataTable(
                            id="table-main-page",
                            editable=True,
                            page_size=10,
                            style_table={"overflowX": "auto"},
                        ),
                        dbc.Container(
                            [
                                REASSIGN_BUTTON := dbc.Button(
                                    "Reassign Columns",
                                ),
                            ],
                            className="d-flex justify-content-end mt-2"
                        ),
                    ],
                ),
            ],
        ),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dcc.Loading(
                            [
                                MAIN_PLOT := dcc.Graph(
                                    id="main-plot"
                                )
                            ],
                        ),
                    ]
                )
            ]
        ),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dcc.Tabs(
                            [
                                dcc.Tab(
                                    [
                                        HALL_TAB,
                                    ],
                                    label="Hall's diagnostic method",
                                ),
                                dcc.Tab(
                                    [
                                        SRT_TAB,
                                    ],
                                    label="Indicator research (SRT)",
                                ),
                                dcc.Tab(
                                    [
                                        CDF_TAB
                                    ],
                                    label="Well flow test",
                                ),
                            ]
                        )
                    ]
                )
            ]
        )
    ],
    id="main_page-content",
    className="d-none flex-column gap-3",
    # className="d-flex flex-column row-gap-2",
)


UPLOAD_COMPONENT = dcc.Upload(
    [
        upload_button := dbc.Button(
            "Drag and Drop or Select table",
            outline=False,
            className="text-center",
            id="table-upload-button"
        )
    ],
    id="table-upload",
    className="container-sm border border-primary-subtle d-flex justify-content-center align-items-center",
    style={"height": "25vh", "width": "50vw"},
)


PAGE_HEADER = dbc.Container(
    children=
    [
        html.H1(
            "geoplot",
            className="float fw-bold text-center mt-3 fs-1 fw-bold",
        ),
        html.Hr(),
        html.H6(
            "TechnoHack IT-GEO 2023"
        ),
        html.H6(
            "Samigullin Linar & Prokopenko Vsevolod"
        ),
        html.A(
            "GitHub", href="https://github.com/Alex1um/Geo"
        ),
        html.Br()
        # html.Hr(),
    ],
    fluid=False,
    className="d-flex flex-column justify-content-center text-center",
)


MAIN_SECTION = html.Section(
    children=[
        UPLOAD_COMPONENT,
        MAIN_COMPONENT,
    ],
    className="container-fluid text-center",
    id="main_page-section"
)
