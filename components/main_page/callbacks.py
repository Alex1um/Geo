from dash import Input, Output, State, dcc, html
from dash_app import app
from components.main_table_config_modal import BT_OK
from components.memory import MAIN_TABLE_CONFIG, SOURCE_TABLE
from components.main_page import MAIN_TABLE, MAIN_COMPONENT, UPLOAD_TABLE, MAIN_PLOT
import base64
import pandas as pd
import io
from typing import Union, Literal
import plotly.graph_objects as go
from tools import make_columns_unique
from components.srt_tab import P_FRAC


@app.callback(
    [
        Output(MAIN_COMPONENT, "is_in"),
        Output(MAIN_COMPONENT, "className"),
        Output(UPLOAD_TABLE, "className"),
        Output(MAIN_TABLE, "data"),
    ],
    [
        Input(MAIN_TABLE_CONFIG, "data"),
    ],
    [
        State(MAIN_COMPONENT, "className"),
        State(UPLOAD_TABLE, "className"),
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
    start_col: int = table_config["start_col"]
    date_colls_names: list[str] | str = table_config["cols_date"]
    date_col_type: Union[Literal["Date"], Literal["Time"]] = table_config["date_type"]
    q_col: str = table_config["col_q"]
    p_col: str = table_config["col_p"]
    nd_col: str = table_config["col_nd"]
    p0_col: str = table_config["col_p0"]
    
    dataframe_src = pd.DataFrame(main_table_data)
    dataframe = dataframe_src.iloc[start_row:, start_col:]
    if start_row > 0:
        columns = dataframe_src.iloc[start_row - 1, start_col:]
    else:
        columns = dataframe_src.columns
    dataframe.columns = make_columns_unique(columns)

    cols = list(filter(bool, [*date_colls_names, q_col, p_col, nd_col, p0_col]))
    dataframe = dataframe[cols]
    if len(date_colls_names) > 1:
        dataframe["DATE"] = dataframe[date_colls_names].apply(lambda x: ' '.join(x.astype(str)), axis=1)
        dataframe.drop(date_colls_names, axis=1, inplace=True)
        dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime)
        # dataframe = dataframe.set_index("DATE").sort_index()
    else:
        # dataframe["DATE"] = dataframe[date_colls_names].apply(lambda x: ' '.join(x.astype(str)), axis=1)
        dataframe = dataframe.rename(columns={date_colls_names[0]: "DATE"})
        if date_col_type != "auto":
            dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime, unit=date_col_type)
        else:
            dataframe["DATE"] = dataframe["DATE"].apply(pd.to_datetime)

        # dataframe = dataframe.set_index(date_colls_names).sort_index()
    dataframe = dataframe.rename(columns={q_col: "Q", p_col: "P", p0_col: "P_0", nd_col: "ND"})

    return [
        True,
        main_classes.replace("d-none", "d-block"),
        upload_classes.replace("d-flex", "d-none"),
        dataframe.to_dict("records"),
    ]


@app.callback(
    [
        Output(SOURCE_TABLE, "data"),
    ],
    Input(UPLOAD_TABLE, "contents"),
    State(UPLOAD_TABLE, "filename"),
    State(UPLOAD_TABLE, "last_modified"),
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

    fig = go.Figure(layout=go.Layout(**{
        "yaxis": {
            "title": "Q",
        },
        "yaxis2": {
            "title": "P",
            "overlaying": "y",
            "side": "right",
            "anchor": "x",
        },
        "yaxis3": {
            "title": "m",
            "overlaying": "y",
            "side": "left",
            "anchor": "free",
        },
    }))
    fig.add_trace(
        go.Scatter(
            x=dataframe.index,
            y=dataframe["Q"],
            name="Flow Rate",
    ))
    fig.add_trace(
        go.Scatter(
            x=dataframe.index,
            y=dataframe["P"],
            name="Pressure",
            yaxis="y2",
    ))
    if "P_0" in dataframe.columns:
        fig.add_trace(
            go.Scatter(
                x=dataframe.index,
                y=dataframe["P_0"],
                name="P0",
                yaxis="y2"
        ))
    if "ND" in dataframe.columns:
        fig.add_trace(
            go.Scatter(
                x=dataframe.index,
                y=dataframe["ND"],
                name="Choke Diameter",
                yaxis="y3",
        ))
        fig.update_layout({
        "xaxis": {
            "domain": [0.065, 1],
        }})
    if p_frac:
        fig.add_trace(
            go.Scatter(
                x=[dataframe.index.min(), dataframe.index.max()],
                y=[p_frac, p_frac],
                mode="lines",
                name="P frac",
                yaxis="y2",
        ))
    return [ 
        fig
    ]
