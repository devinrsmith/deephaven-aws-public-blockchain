from deephaven import dtypes, parquet
from deephaven.column import Column, ColumnType
from deephaven.experimental import s3
from deephaven.table import Table

import os
from datetime import datetime, timedelta
from functools import cache


def _int_if(x):
    return int(x) if x else None


# static now, maybe make dynamic w/ listener in future if necessary?
# Native data iteration from python: https://github.com/deephaven/deephaven-core/issues/5186
_s3_instructions = s3.S3Instructions(
    "us-east-2",
    anonymous_access=True,
    read_ahead_count=_int_if(os.getenv("S3_READ_AHEAD_COUNT")),
    fragment_size=_int_if(os.getenv("S3_FRAGMENT_SIZE")),
    read_timeout=timedelta(seconds=_int_if(os.getenv("S3_READ_TIMEOUT_SECS")) or 10),
)


@cache
def read_transactions() -> tuple[Table, Table]:
    # We need to be conservative with what data we actually read.
    # AWS writes out intraday data into their own parquet files, and then consolidates it into a single file at the end of the day.
    # We currently assume that parquet files will not be deleted, so we need to only pick up the fully-finished daily files.
    # v1.0/btc/transactions/date=2024-05-18/part-00000-f936a833-d06b-4f62-a3e2-990b0facdc57-c000.snappy.parquet
    # v1.0/btc/transactions/date=2024-05-19/part-00000-e311a07f-5226-4774-8eab-d665f8cb60aa-c000.snappy.parquet
    # v1.0/btc/transactions/date=2024-05-20/part-00000-17fda466-ef62-43f4-9d9b-976498496cfe-c000.snappy.parquet
    # v1.0/btc/transactions/date=2024-05-21/844369.snappy.parquet
    # v1.0/btc/transactions/date=2024-05-21/844370.snappy.parquet
    # v1.0/btc/transactions/date=2024-05-21/844371.snappy.parquet
    # v1.0/btc/transactions/date=2024-05-21/844372.snappy.parquet
    # A more generic approach to this would be to allow some sort of regex matching syntax; ie, "part-.*", or generic callback that allows caller to decide whether a file should be included.
    # The consolidated files seem to be written a bit after 00:30 UTC. We should err on the conservative side, and will give it a full hour.
    current_date = (datetime.utcnow() - timedelta(hours=1)).date()
    transactions = parquet.read(
        "s3://aws-public-blockchain/v1.0/btc/transactions/",
        special_instructions=_s3_instructions,
        file_layout=parquet.ParquetFileLayout.KV_PARTITIONED,
        table_definition=[
            Column("date", dtypes.string, column_type=ColumnType.PARTITIONING),
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
    ).where([f"date<`{current_date}`"])
    # Returning both the source aware and the partition table; it seems that
    #   source_aware = parquet.read(...)
    #   partitioned = source_aware.partition_by(["PartitionColumn"])
    #   partitioned_merge = partitioned.merge()
    # does not get you back the source_aware table
    return transactions, transactions.partition_by(["date"])


transactions, transactions_by_date = read_transactions()
