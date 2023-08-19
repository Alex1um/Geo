from dash import dcc

TABLE_CONFIG = dcc.Store(id="table-config", storage_type="session")
SOURCE_TABLE = dcc.Store(id="source-table", storage_type="session")
