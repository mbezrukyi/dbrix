import functools

from pyspark.sql import DataFrame, functions as F
from pyspark.sql.avro import functions as AF

from .helper import Helper
from .resolver import SchemaResolver


class Parser:
    def __init__(
        self,
        df: DataFrame,
        resolver: SchemaResolver,
    ):
        self._df = df
        self._resolver = resolver

    def parse(self) -> DataFrame:
        return functools.reduce(
            lambda df1, df2: df1.unionByName(df2, allowMissingColumns=True),
            (
                Helper.enhanced(self._df)
                .filter(F.col('schema_id') == schema_id)
                .withColumn(
                    "value",
                    AF.from_avro(
                        F.expr("substring(value, 6)"),
                        schema_str,
                        options={"mode": "PERMISSIVE"}
                    )
                )
                .select('value.*', '*')
                for schema_id, schema_str in self._resolver.resolve(Helper.schemas(self._df)).items()
            )
        )
