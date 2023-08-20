from dash import Dash, Input, Output, State
# from dash_core_components import Upload
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash import dash_table


def generate_upload_table(
    app: Dash,
    config_store: dcc.Store,
    data_input: Input,
    open_triggers: list[Input],
    modal_inputs: list[dbc.Input],
    input_groups: list[dbc.InputGroup],
    required_inputs: list[dbc.Input],
) -> (dbc.Modal, dbc.Button, dbc.Button):

    content = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            table_start := dbc.Input(type="number", value=0),
                        ],
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            preview_table := dash_table.DataTable(
                                style_table={"overflowX": "auto"},
                                page_size=10,
                            ),
                        ],
                    ),
                ],
            ),
            dbc.Row(
                input_groups
            ),
        ],
        className="gap-2",
        fluid=True,
    )

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
                children=content,
            ),
            dbc.ModalFooter(
                [
                    bt_cancel := dbc.Button(
                        "Cancel",
                        color="secondary",
                    ),
                    bt_ok := dbc.Button(
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

    @app.callback(
        [
            Output(table_start, "value")
        ],
        [
            Input(bt_cancel, "n_clicks"),
            Input(bt_ok, "data"),
        ],
        prevent_initial_call=True,
    )
    def on_cancel(_, current_config: dict):
        if current_config:
            return current_config["start_row"],
        else:
            return 0,


    @app.callback(
        [
            Output(config_store, "data"),
        ],
        Input(bt_ok, "n_clicks"),
        [
            State(table_start, "value"),
            *(State(inp, "value") for inp in modal_inputs)
        ],
        prevent_initial_call=True,
    )
    def on_ok(
            _,
            start_row: int,
            *args
    ):
        data = {
            "start_row": start_row,
            **{name:value for name, value in zip(modal_inputs, args)}
        }
        return [
            data,
        ]

    if required_inputs:
        @app.callback(
            [
                Output(bt_ok, "disabled"),
                Output(bt_ok, "outline"),
            ],
            [
                Input(inp, "value") for inp in required_inputs
            ],
            prevent_initial_call=True,
        )
        def check_ok(*args):
            is_ready = not all(args)
            return [
                is_ready,
                is_ready,
            ]


    @app.callback(
        [
            Output(preview_table, "data"),
        ],
        [
            Input(table_start, "value"),
            data_input,
        ],
        [
            State(table_start, "value"),
            State(preview_table, "data"),
            State(config_store, "data"),
        ],
        prevent_initial_call=True,
    )
    def srt_on_start_change_or_init_on_source_data(
            new_start,
            all_data,
            old_start,
            preview_data,
            current_config,
    ):
        dataframe_source = pd.DataFrame(all_data)
        data = []
        cols = []
        if new_start >= 0:
            new_dataframe = dataframe_source.iloc[new_start:new_start + 5]
            if new_start == 0:
                new_dataframe.columns = dataframe_source.columns
            else:
                new_dataframe.columns = dataframe_source.iloc[new_start - 1]
            cols = new_dataframe.columns.array
            data = new_dataframe.to_dict("records")
        if current_config and current_config["start_row"] == new_start:
            return [
                data,
                cols,
                cols,
                cols,
                current_config["cols_date"],
                current_config["col_q"],
                current_config["col_p"],
            ]
        else:
            return [
                data,
                cols,
                cols,
                cols,
                None,
                None,
                None,
            ]
