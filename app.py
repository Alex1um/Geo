import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import pyfigure, pyfunc, pylayout, pylayoutfunc
from dash import dcc, html, Input, Output, State
from pathlib import Path


# APP
app = dash.Dash(
    suppress_callback_exceptions=False,
    external_stylesheets=[getattr(dbc.themes, "COSMO"), "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"]
)
server = app.server

app.layout = dbc.Container(
    [
        pylayout.HTML_TITLE,
        pylayout.HTML_ROW_BUTTON_UPLOAD,
        pylayout.HTML_ROW_TABLE,
        pylayout.HTML_ROW_BUTTON_VIZ,
        pylayout.HTML_ROW_OPTIONS_GRAPH_RAINFALL,
        pylayout.HTML_ROW_GRAPH_ONE,
    ],
    fluid=True,
    className="dbc",
)

@app.callback(
    [
        Output("row-table-uploaded", "children"),
        Output("dcc-upload", "disabled"),
        Output("button-upload", "disabled"),
        Output("button-visualize", "disabled"),
        Output("button-visualize", "outline"),
    ],
    Input("dcc-upload", "contents"),
    State("dcc-upload", "filename"),
    State("dcc-upload", "last_modified"),
    Input("button-skip", "n_clicks"),
    prevent_initial_call=True,
)
def callback_upload(content, filename, filedate, _):
    ctx = dash.callback_context

    if content is not None:
        children, dataframe = pyfunc.parse_upload_data(content, filename, filedate)

    if ctx.triggered[0]["prop_id"] == "button-skip.n_clicks":
        dataframe = pd.read_csv(
            Path(r"./inj_well_36.csv"), index_col=0, parse_dates=True
        )
        filename = None
        filedate = None

    upload_disabled = False
    button_upload_disabled = False
    button_viz_disabled = True
    button_viz_outline = True

    if dataframe is not None:
        editable = [False] + [True] * len(dataframe.columns)
        children = pylayoutfunc.create_table_layout(
            dataframe,
            "output-table",
            filename=filename,
            filedate=filedate,
            editable=editable,
            renamable=True,
        )
        upload_disabled = False
        button_upload_disabled = False
        button_viz_disabled = False
        button_viz_outline = False

    return [
        children,
        upload_disabled,
        button_upload_disabled,
        button_viz_disabled,
        button_viz_outline,
    ]


@app.callback(
    [
        Output("graph-rainfall", "figure"),
        Output("row-button-download-csv", "style"),
        Output("graph-rainfall", "config"),
        Output("container-graphbar-options", "style"),
    ],
    Input("button-visualize", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
    State("radio-graphbar-options", "value"),
    State("graph-selector", "value"),
    prevent_initial_call=True,
)
def callback_visualize(_, table_data, table_columns, graphbar_opt, graph_selector):
    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

    row_download_table_style = {"visibility": "visible"}
    row_graph_config = {"staticPlot": False}
    row_graphbar_options_style = {"visibility": "hidden"}

    if graph_selector == "Hall":
        pass
    elif graph_selector == "SRT":
        pass

    if dataframe.size > (366 * 8):
        fig = pyfigure.figure_scatter(dataframe)
    else:
        row_graphbar_options_style = {"visibility": "visible"}
        if graphbar_opt in ["group", "stack"]:
            fig = pyfigure.figure_bar(dataframe, graphbar_opt)
        else:
            fig = pyfigure.figure_scatter(dataframe)

    return [
        fig,
        row_download_table_style,
        row_graph_config,
        row_graphbar_options_style,
    ]


@app.callback(
    Output("download-csv", "data"),
    Input("button-download-csv", "n_clicks"),
    prevent_initial_call=True,
)
def callback_download_table(_, table_data, table_columns):
    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)
    return dcc.send_data_frame(dataframe.to_csv, "derived_table.csv")


if __name__ == "__main__":
    app.run_server(debug=True)
