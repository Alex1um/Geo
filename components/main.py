from dash import dash_table
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc


MAIN_CONTENT = html.Div(
    [
        MAIN_TABLE := dash_table.DataTable(
            id="table-main",
            style_table={"display": "block"}
        ),
        dbc.Button(
            "Reassign Columns"
        )
    ],
    id="main-content",
    style={"display": "none"}
)
