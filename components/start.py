from dash import dash_table
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from components.upload import UPLOAD_COMPONENT
from components.main import MAIN_CONTENT
from dash_app import app


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
            "GitHub", href="https://github.com/Alex1um/Geo>GitHub"
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
    id="main-section"
)


@app.callback(
    [
        Output(UPLOAD_COMPONENT, "className"),
    ],
    Input(MAIN_CONTENT, "style"),
    State(UPLOAD_COMPONENT, "className"),
    prevent_initial_call=True,
)
def on_upload_hide(new_style, class_name):
    return [
        class_name.replace("d-flex", "d-none"),
    ]
