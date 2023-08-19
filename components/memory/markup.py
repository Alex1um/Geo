from dash import dcc

_storage_type = "session"
_storage_type_srt = "memory"

MAIN_TABLE_CONFIG = dcc.Store(id="table-config", storage_type=_storage_type, data=None)
SOURCE_TABLE = dcc.Store(id="source-table", storage_type=_storage_type, data=None)
SRT_TABLE = dcc.Store(id="srt-table", storage_type=_storage_type_srt, data=None)
SRT_TABLE_CONFIG = dcc.Store(id="srt-table-config", storage_type=_storage_type_srt, data=None)
