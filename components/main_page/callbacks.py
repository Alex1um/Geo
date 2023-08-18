from dash import Input, Output, State, dcc, html
from dash_app import app
from components.main_table_config_modal import BT_OK, TABLE_CONFIG
from components.main_page import MAIN_TABLE, MAIN_COMPONENT, UPLOAD_COMPONENT, SOURCE_TABLE
import base64
import pandas as pd
import io
from typing import Union, Literal


@app.callback(
    [
        Output(MAIN_COMPONENT, "className"),
        Output(UPLOAD_COMPONENT, "className"),
        Output(MAIN_TABLE, "style_data_conditional"),
        Output(MAIN_TABLE, "data"),
    ],
    [
        Input(TABLE_CONFIG, "data"),
    ],
    [
        State(MAIN_COMPONENT, "className"),
        State(UPLOAD_COMPONENT, "className"),
        State(SOURCE_TABLE, "data"),
    ],
    prevent_initial_call=True,
)
def on_config_ok(
    table_config: dict,
    main_classes: str,
    upload_classes: str,
    main_table_data,
):
    start_row: int = table_config["start_row"]
    date_colls_names: list[str] = table_config["cols_date"]
    date_col_type: Union[Literal["Date"], Literal["Time"]] = table_config["date_type"]
    q_col: str = table_config["col_q"]
    p_col: str = table_config["col_p"]
    nd_col: str = table_config["col_nd"]
    dataframe = pd.DataFrame(main_table_data)
    if start_row > 0:
        dataframe.columns = dataframe.iloc[start_row - 1]
    else:
        dataframe.columns = dataframe.columns
    dataframe = dataframe.iloc[start_row:]

    style_data_conditional=[
        *[{
            "if": {
                "column_id": col_date_component
            },
            "backgroundColor": "gray",
        } for col_date_component in date_colls_names],
        {
            "if": {
                "column_id": q_col
            },
            "backgroundColor": "gray",
        },
        {
            "if": {
                "column_id": p_col
            },
            "backgroundColor": "gray",
        },
    ]

    if nd_col:
        style_data_conditional.append(
            {
                "if": {
                    "column_id": nd_col
                },
                "backgroundColor": "gray",
            }
        )
    
    return [
        main_classes.replace("d-none", "d-flex"),
        upload_classes.replace("d-flex", "d-none"),
        style_data_conditional,
        dataframe.to_dict("records"),
    ]


@app.callback(
    [
        Output(SOURCE_TABLE, "data"),
    ],
    Input(UPLOAD_COMPONENT, "contents"),
    State(UPLOAD_COMPONENT, "filename"),
    State(UPLOAD_COMPONENT, "last_modified"),
    prevent_initial_call=True,
)
def on_upload(content, filename, filedate):
    # global dataframe_source

    dataframe_source = None

    if content is not None:
        _, content_string = content.split(",")

        decoded = base64.b64decode(content_string)

        if filename.endswith(".csv"):
            dataframe_source = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            dataframe_source = pd.read_excel(decoded)

    return [
        dataframe_source.to_dict("records"),
    ]
