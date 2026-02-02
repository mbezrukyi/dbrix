from pyspark.sql import DataFrame, functions as F


class ReservationsHelper:
    COLUMN = 'schema_id'

    @classmethod
    def enhanced(cls, df: DataFrame) -> DataFrame:
        return (
            df
            .withColumn(
                cls.COLUMN,
                F.expr('conv(hex(substring(value, 1, 5)), 16, 10)')
            )
        )

    @classmethod
    def schemas(cls, df: DataFrame) -> list[str]:
        return (
            getattr(row, cls.COLUMN)
            for row in (
                cls.enhanced(df)
                .select(cls.COLUMN)
                .distinct()
                .collect()
            )
        )
