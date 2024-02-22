import deephaven.ui as ui

from deephaven import csv, dtypes, parquet
from deephaven.column import Column
from deephaven.numpy import to_numpy
from deephaven.ui import use_state
from deephaven.experimental import s3
from deephaven.table import Table

import os
from datetime import timedelta
from functools import cache

# static now, maybe make dynamic w/ listener in future if necessary?
_uris = {date: s3Uri for date, s3Uri in to_numpy(csv.read("/uris.csv"))}
_s3_instructions = s3.S3Instructions(
    "us-east-2",
    anonymous_access=True,
    read_ahead_count=os.getenv("S3_READ_AHEAD_COUNT", 8),
    fragment_size=os.getenv("S3_FRAGMENT_SIZE", 65536),
    read_timeout=timedelta(seconds=10),
)


@cache
def read_transactions(s3_uri: str) -> Table:
    return parquet.read(
        s3_uri,
        special_instructions=_s3_instructions,
        file_layout=parquet.ParquetFileLayout.SINGLE_FILE,
        table_definition=[
            Column("last_modified", dtypes.Instant),
            Column("output_value", dtypes.float64),
            Column("fee", dtypes.float64),
            Column("input_value", dtypes.float64),
            Column("version", dtypes.int64),
            Column("size", dtypes.int64),
            Column("block_number", dtypes.int64),
            Column("index", dtypes.int64),
            Column("virtual_size", dtypes.int64),
            Column("lock_time", dtypes.int64),
            Column("input_count", dtypes.int64),
            Column("output_count", dtypes.int64),
            Column("is_coinbase", dtypes.bool_),
            # TODO: parameterize this so users can view w/ checkbox?
            # Column("hash", dtypes.string),
            # Column("block_hash", dtypes.string),
        ],
    )


@ui.component
def transactions_component():
    # todo: dropdown based on transactions.keys()?
    # https://github.com/deephaven/deephaven-plugins/issues/200
    value, set_value = use_state(next(iter(reversed(_uris.keys()))))
    # todo: handle out-of-bounds
    s3_uri = _uris[value]
    s3_table = read_transactions(s3_uri)
    return ui.flex(
        ui.text_field(value=value, on_change=set_value),
        s3_table,
        direction="column",
        flex_grow=1,
    )


transactions = transactions_component()
