import functools

from pyspark.sql import DataFrame, functions as F
from pyspark.sql.avro import functions as AF

from .resolver import SchemaResolver


class FieldParser:
    def __init__(self, resolver: SchemaResolver):
        self._resolver = resolver

    def apply(self, df: DataFrame) -> DataFrame:
        enhanced = self._enhance(df).cache()

        schema_ids = [
            getattr(row, self.COLUMN)
            for row in (
                enhanced
                .select(self.COLUMN)
                .distinct()
                .collect()
            )
        ]

        return functools.reduce(
            lambda df1, df2: df1.unionByName(df2, allowMissingColumns=True),
            (
                self._decode(
                    enhanced.filter(F.col(self.COLUMN) == schema_id),
                    schema_id,
                )
                for schema_id in schema_ids
            ),
        )

    def _enhance(self, df: DataFrame) -> DataFrame:
        return df.withColumn(
            self.COLUMN,
            F.expr(f'conv(hex(substring({self.FIELD}, 1, 5)), 16, 10)'),
        )

    def _decode(self, df: DataFrame, schema_id: str) -> DataFrame:
        return df.withColumn(
            self.FIELD,
            AF.from_avro(
                F.expr(f'substring({self.FIELD}, 6)'),
                self._resolver.resolve(schema_id),
                options={'mode': 'PERMISSIVE'},
            ),
        )

    def parse(self, df: DataFrame) -> DataFrame:
        return self.apply(df).select('*', f'{self.FIELD}.*')


class KeyParser(FieldParser):
    FIELD = 'key'
    COLUMN = 'key_schema_id'


class ValueParser(FieldParser):
    FIELD = 'value'
    COLUMN = 'value_schema_id'
