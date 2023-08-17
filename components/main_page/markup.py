from dash import dash_table, html
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

from components.upload import UPLOAD_COMPONENT

MAIN_CONTENT = html.Div(
    [
        MAIN_TABLE := dash_table.DataTable(
            id="table-main_page",
            style_table={"display": "block"}
        ),
        REASSIGN_BUTTON := dbc.Button(
            "Reassign Columns"
        )
    ],
    id="main_page-content",
    style={"display": "none"}
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
        MAIN_CONTENT,
    ],
    className="container-fluid text-center",
    id="main_page-section"
)
