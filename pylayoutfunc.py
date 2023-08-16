from __future__ import annotations
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from datetime import datetime
import dash_bootstrap_components as dbc


def create_table_layout(
    dataframe,
    idtable,
    filename=None,
    filedate=None,
    editable: list | bool = False,
    deletable=True,
    renamable=False,
):
    from collections.abc import Iterable

    new_dataframe = dataframe.rename_axis("DATE").reset_index()
    new_dataframe.DATE = new_dataframe.DATE.dt.date
    # new_dataframe = dataframe

    editable = (
        editable
        if isinstance(editable, Iterable)
        else [editable] * len(new_dataframe.columns)
    )

    table = dash_table.DataTable(
        id=idtable,
        columns=[
            {
                "name": i,
                "id": i,
                "deletable": deletable,
                "renamable": renamable,
                "editable": edit_col,
            }
            for i, edit_col in zip(new_dataframe.columns, editable)
        ],
        data=new_dataframe.to_dict("records"),
        page_size=10,
        cell_selectable=True,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
        style_header={"font-size": 20, "textAlign": "center", "font-weight": "bold"},
    )
    add_title = (
        f' ({filename}:{datetime.fromtimestamp(filedate).strftime("%Y-%m-%d")})'
        if (filename is not None) and (filedate is not None)
        else ""
    )
    title_table = f"DATA TABLE" + add_title
    return html.H2(title_table, className="text-center"), table

