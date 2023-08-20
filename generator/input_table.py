from dash import Dash, Input, Output
# from dash_core_components import Upload
import dash_bootstrap_components as dbc
import dash_core_components as dcc

def generate_upload_table(
    app: Dash,
    params_output: Output,
    source_output: Output,
    upload_component: dcc.Upload,
    open_triggers: list[Input],
    modal_inputs: list,
) -> (dbc.Modal, dbc.Button, dbc.Button):
    
    config_modal = dbc.Modal(
    [
        dbc.ModalHeader(
            [
                dbc.ModalTitle(
                    "Configure Table",
                ),
            ],
            close_button=False,
        ),
        dbc.ModalBody(
            children=CONFIG_MODAL_CONTENT,
        ),
        dbc.ModalFooter(
            [
                BT_CANCEL := dbc.Button(
                    "Cancel",
                    color="secondary",
                ),
                BT_OK := dbc.Button(
                    "OK",
                    color="primary",
                    outline=True,
                    disabled=True,
                )
            ]
        )
    ],
    size="xl",

)



