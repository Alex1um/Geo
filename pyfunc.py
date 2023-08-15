import io
import pandas as pd
from dash import html
import numpy as np


def parse_upload_data(content, filename, filedate):
    content_string: str
    _, content_string = content.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if filename.endswith(".csv"):
            dataframe = pd.read_csv(
                io.StringIO(decoded.decode("utf-8")), index_col=0, parse_dates=True,
                # usecols=["date", "Qприем ТМ", "Рбуф", "Dшт"]
            )
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):

            dataframe = pd.read_excel(
                decoded, index_col=0, parse_dates=[[0, 1]],
            )
        else:
            return (
                html.Div(
                    ["Unknown extension"],
                    className="text-center bg-danger text-white fs-4",
                ),
                None,
            )
    except Exception as e:
        print(e)
        return html.Div([f"There was an error processing this file. {e}"]), None

    return html.Div(["File Diterima"]), dataframe


def transform_to_dataframe(
    table_data,
    table_columns,
):

    columns = pd.Index([item["name"] for item in table_columns])
    dataframe = pd.DataFrame(table_data, columns=columns)

    dataframe["DATE"] = pd.to_datetime(dataframe.DATE)
    dataframe = dataframe.set_index("DATE").sort_index()

    dataframe = dataframe.apply(pd.to_numeric, errors="coerce")

    return dataframe
