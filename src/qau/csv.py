from typing import Any

from pyspark.sql import DataFrame, SparkSession


def read(path: str, **options: Any) -> DataFrame:
    return (
        SparkSession.builder.getOrCreate()
        .read
        .option('nullValue', None)
        .csv(path=path, **options)
    )
