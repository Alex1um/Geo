from dash import dcc

_storage_type = "memory"
_storage_type_srt = "memory"

MAIN_TABLE_CONFIG = dcc.Store(id="table-config", storage_type=_storage_type)
SOURCE_TABLE = dcc.Store(id="source-table", storage_type=_storage_type)
SRT_TABLE = dcc.Store(id="srt-table", storage_type=_storage_type_srt)
SRT_TABLE_CONFIG = dcc.Store(id="srt-table-config", storage_type=_storage_type_srt)
GDIS_PARAMS = dcc.Store(id="gdis-params", storage_type="session")
