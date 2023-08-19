from dash import Input, Output, State, dcc, html
from dash_app import app
from components.main_table_config_modal import BT_OK, TABLE_CONFIG
from components.main_page import MAIN_TABLE, MAIN_COMPONENT, UPLOAD_COMPONENT, SOURCE_TABLE, MAIN_PLOT
import base64
import pandas as pd
import io
from typing import Union, Literal
import plotly.graph_objects as go


@app.callback(
    [
        Output(MAIN_COMPONENT, "className"),
        Output(UPLOAD_COMPONENT, "className"),
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
    date_colls_names: list[str] | str = table_config["cols_date"]
    date_col_type: Union[Literal["Date"], Literal["Time"]] = table_config["date_type"]
    q_col: str = table_config["col_q"]
    p_col: str = table_config["col_p"]
    nd_col: str = table_config["col_nd"]
    p0_col: str = table_config["col_p0"]
    
    dataframe = pd.DataFrame(main_table_data)
    if start_row > 0:
        dataframe.columns = dataframe.iloc[start_row - 1]
    else:
        dataframe.columns = dataframe.columns
    dataframe = dataframe.iloc[start_row:]
    
    cols = [q_col, p_col, nd_col, p0_col]
    if isinstance(date_colls_names, list):
        cols.extend(date_colls_names)
    else:
        cols.append(date_colls_names)
    cols = list(filter(bool, cols))
    dataframe = dataframe[cols]
    if date_col_type == "Date":
        dataframe["DATE"] = dataframe[date_colls_names].apply(lambda x: ' '.join(x.astype(str)), axis=1)
        dataframe.drop(date_colls_names, axis=1, inplace=True)
        dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime)
        # dataframe = dataframe.set_index("DATE").sort_index()
    else:
        # dataframe["DATE"] = dataframe[date_colls_names].apply(lambda x: ' '.join(x.astype(str)), axis=1)
        dataframe = dataframe.rename(columns={date_colls_names: "DATE"})
        dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime, unit="s")

        # dataframe = dataframe.set_index(date_colls_names).sort_index()
    dataframe = dataframe.rename(columns={q_col: "Q", p_col: "P", p0_col: "P_0", nd_col: "ND"})

    return [
        main_classes.replace("d-none", "d-flex"),
        upload_classes.replace("d-flex", "d-none"),
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

from components.hall_tab import HALL_GRAPH
from components.srt_tab import P_FRAC

@app.callback(
    [
        Output(MAIN_PLOT, "figure")
    ],
    [
        Input(MAIN_TABLE, "data"),
        Input(P_FRAC, "value"),
    ],
    [
        State(MAIN_PLOT, "figure"),
    ],
    prevent_initial_call=True,
)
def main_graph_update(table_data, p_frac, old_fig):
    
    dataframe = pd.DataFrame(table_data)
    dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime)
    dataframe = dataframe.set_index("DATE").sort_index()
    
    data = [
        go.Scatter(x=dataframe.index, y=dataframe[col], mode="lines", name=col)
        for col in dataframe.columns
    ]
    if p_frac:
        data.append(
            go.Scatter(x=[dataframe.index.min(), dataframe.index.max()], y=[p_frac, p_frac], mode="lines", name="P_frac")
            )
    
    fig = go.Figure(data)

    return [ 
        fig
    ]
