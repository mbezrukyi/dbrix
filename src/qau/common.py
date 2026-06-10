from enum import Enum

from pyspark.sql import DataFrame, functions as F, SparkSession
from pyspark.sql.types import ArrayType, StructType


class Env(Enum):
    DEV = 'tst'
    PROD = 'prd'
    QA = 'stg'


class Path:
    TEMPLATE = '/Volumes/{catalog}/artifacts/configs/mnt/{mount}/artifacts/qau/{file}'

    @classmethod
    def build(cls, env: Env, file: str) -> str:
        return cls.TEMPLATE.format(
            catalog=SparkSession.builder.getOrCreate().catalog.currentCatalog(),
            mount=f'{env.value}-configuration-realtime',
            file=file,
        )


def flat(df: DataFrame) -> DataFrame:
    while any(isinstance(field.dataType, (ArrayType, StructType)) for field in df.schema):
        cols = []

        for field in df.schema:
            if isinstance(field.dataType, StructType):
                for nested in field.dataType:
                    cols.append(F.col(f'{field.name}.{nested.name}').alias(f'{field.name}__{nested.name}'))
            elif isinstance(field.dataType, ArrayType):
                cols.append(F.explode_outer(F.col(field.name)).alias(field.name))
            else:
                cols.append(F.col(field.name).cast('STRING'))

        df = df.select(*cols)

    return df


def unpivot(df: DataFrame) -> DataFrame:
    return df.select(F.stack(
        F.lit(len(df.columns)),
        *[
            x
            for col in df.columns
            for x in (F.lit(col), col)
        ]
    ).alias('key', 'value'))
