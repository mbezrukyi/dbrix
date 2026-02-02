from typing import Protocol

from pyspark.sql import DataFrame, functions as F
from pyspark.sql.avro.functions import from_avro, to_avro


class KafkaParser(Protocol):
    def to(self, df: DataFrame) -> DataFrame:
        ...

    def from_(self, df: DataFrame) -> DataFrame:
        ...


class CommonKafkaParser:
    def to(self, df: DataFrame) -> DataFrame:
        return df.withColumn('value', F.encode(F.col('value'), 'utf-8'))

    def from_(self, df: DataFrame) -> DataFrame:
        return df.withColumn('value', F.decode(F.col('value'), 'utf-8'))


class AvroKafkaParser:
    def __init__(self, schema: str):
        self._schema = schema

    def to(self, df: DataFrame, schema_id: int) -> DataFrame:
        return (
            df
            .withColumn('value', to_avro(F.col('value'), self._schema))
            .withColumn('value', F.expr(f'concat(unhex("{hex(schema_id).split("x")[1].zfill(10)}"), value)'))
        )

    def from_(self, df: DataFrame) -> DataFrame:
        return (
            df.withColumn('schema_id', F.expr('conv(hex(substring(value, 1, 5)), 16, 10)'))
            .withColumn(
                'value',
                from_avro(
                    F.expr('substring(value, 6)'),
                    self._schema,
                    options={'mode': 'PERMISSIVE'}
                )
            )
        )
