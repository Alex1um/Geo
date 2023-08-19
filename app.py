import dash_bootstrap_components as dbc
import pandas as pd
from dash_app import app
from components import *

# dataframe_source: pd.DataFrame = None
# dataframe: pd.DataFrame = None

# APP
# app = dash.Dash(
#     suppress_callback_exceptions=False,
#     external_stylesheets=[getattr(dbc.themes, "COSMO"),
#                           "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"],
# )
server = app.server

app.layout = dbc.Container(
    [
        BOOTSTRAP_CSS,
        BOOTSTRAP_JS,
        MAIN_TABLE_CONFIG,
        SOURCE_TABLE,
        PAGE_HEADER,
        MAIN_SECTION,
        CONFIG_MODAL,
        # pylayout.HTML_TITLE,
        # pylayout.HTML_ROW_BUTTON_UPLOAD,
        # pylayout.TABLE_BEGIN,
        # pylayout.HTML_ROW_TABLE,
        # pylayout.HTML_ROW_BUTTON_VIZ,
        # pylayout.HTML_ROW_GRAPH_ONE,
    ],
    fluid=True,
    className="dbc",
)

if __name__ == "__main__":
    app.run_server(debug=True)
    