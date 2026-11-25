from pyspark.sql import DataFrame, functions as F
from pyspark.sql.types import ArrayType, StructType


def flatten(df: DataFrame) -> DataFrame:
    while any(
        isinstance(field.dataType, (ArrayType, StructType))
        for field in df.schema
    ):
        columns = []

        for field in df.schema:
            if isinstance(field.dataType, StructType):
                for nested in field.dataType:
                    columns.append(
                        F.col(f'{field.name}.{nested.name}')
                        .alias(f'{field.name}__{nested.name}')
                    )
            elif isinstance(field.dataType, ArrayType):
                columns.append(F.explode_outer(F.col(field.name)).alias(field.name))
            else:
                columns.append(F.col(field.name).cast('STRING'))

        df = df.select(*columns)

    return df


def unpivot(df: DataFrame) -> DataFrame:
    return df.select(
        F.stack(
            F.lit(len(df.columns)),
            *[
                name_or_value
                for column in df.columns
                for name_or_value in (F.lit(column), column)
            ],
        ).alias('key', 'value')
    )
