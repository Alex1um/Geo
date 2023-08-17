from dash import Output, Input, State

from components.main_page import MAIN_CONTENT
from components.upload import UPLOAD_COMPONENT
from dash_app import app


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
