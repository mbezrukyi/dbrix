from typing import Any

from pyspark.sql import DataFrame, SparkSession


class CSVReader:
    def __init__(self, path: str, **options: Any):
        self.path = path
        self.options = options

    def read(self) -> DataFrame:
        return (
            SparkSession.builder.getOrCreate()
            .read
            .option('nullValue', None)
            .csv(
                path=self.path,
                **self.options,
            )
        )
