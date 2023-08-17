from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dash_app import app
import pandas as pd
import base64
from components.main import MAIN_TABLE
from components.table_config_dialog import UPLOAD_MODAL
from components.table_config_dialog import table_start
import io


UPLOAD_COMPONENT = dbc.Container(
    [
        UPLOAD_AREA := dcc.Upload(
            [
                upload_button := dbc.Button(
                    "Drag and Drop or select table",
                    outline=False,
                    className="text-center",
                    id="table-upload-button"
                )
            ],
            id="table-upload",
        ),
    ],
    className="container-sm border border-primary-subtle d-flex justify-content-center align-items-center",
    style={"height": "25vh", "width": "50vw"},
)


@app.callback(
    [
        Output(UPLOAD_MODAL, "is_open", allow_duplicate=True),
        Output(MAIN_TABLE, "data", allow_duplicate=True),
        Output(table_start, "value"),
    ],
    Input(UPLOAD_AREA, "contents"),
    State(UPLOAD_AREA, "filename"),
    State(UPLOAD_AREA, "last_modified"),
    prevent_initial_call=True,
)
def callback_upload(content, filename, filedate):
    # global dataframe_source

    go_next = False
    dataframe_source = None

    if content is not None:
        _, content_string = content.split(",")

        decoded = base64.b64decode(content_string)

        if filename.endswith(".csv"):
            dataframe_source = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            dataframe_source = pd.read_excel(decoded)

    val = -1

    if dataframe_source is not None:
        go_next = True
        val = 0

    return [
        go_next,
        dataframe_source.to_dict("records"),
        val
    ]
