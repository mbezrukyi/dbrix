import functools
from dataclasses import dataclass

from confluent_kafka.schema_registry import SchemaRegistryClient
from pyspark.sql import DataFrame, functions as F
from pyspark.sql.avro.functions import from_avro, to_avro


HEADER_SIZE = 5


@dataclass
class RegistryConfig:
    url: str
    auth: str


def decode(df: DataFrame, column: str, config: RegistryConfig) -> DataFrame:
    registry = SchemaRegistryClient({
        'url': config.url,
        'basic.auth.user.info': config.auth,
    })
    schema_id_column = f'{column}_schema_id'

    identified = df.withColumn(
        schema_id_column,
        F.expr(f'conv(hex(substring({column}, 1, {HEADER_SIZE})), 16, 10)'),
    ).cache()

    schema_ids = [
        row[schema_id_column]
        for row in identified.select(schema_id_column).distinct().collect()
    ]

    return functools.reduce(
        lambda decoded, other: decoded.unionByName(other, allowMissingColumns=True),
        (
            identified
            .filter(F.col(schema_id_column) == schema_id)
            .withColumn(
                column,
                from_avro(
                    F.expr(f'substring({column}, {HEADER_SIZE + 1})'),
                    registry.get_schema(int(schema_id)).schema_str,
                    options={'mode': 'PERMISSIVE'},
                ),
            )
            for schema_id in schema_ids
        ),
    )


def encode(df: DataFrame, column: str, schema: str, schema_id: int) -> DataFrame:
    return df.withColumn(
        column,
        F.concat(
            F.unhex(F.lit(f'00{schema_id:08x}')),
            to_avro(F.col(column), schema),
        ),
    )
