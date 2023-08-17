import dash_bootstrap_components as dbc
from dash import dcc

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
