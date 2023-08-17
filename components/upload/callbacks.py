import base64
import io

import pandas as pd
from dash import Output, Input, State

from components.main_page import MAIN_TABLE
from components.main_table_modal import UPLOAD_MODAL, table_start
from components.upload import UPLOAD_AREA
from dash_app import app


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
