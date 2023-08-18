from dash import dash_table, html
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

MAIN_COMPONENT = html.Div(
    [
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        MAIN_TABLE := dash_table.DataTable(
                            id="table-main_page",
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
    ],
    id="main_page-content",
    className="d-none flex-column",
    # className="d-flex flex-column",
)


UPLOAD_COMPONENT = dcc.Upload(
    [
        upload_button := dbc.Button(
            "Drag and Drop or select table",
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
            "GeoPROD",
            className="float fw-bold text-center mt-3 fs-1 fw-bold",
        ),
        html.H6(
            "TechnoHack 2023"
        ),
        html.A(
            "GitHub", href="https://github.com/Alex1um/Geo"
        ),
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
