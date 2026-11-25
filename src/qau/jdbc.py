from dataclasses import dataclass

from pyspark.sql import DataFrame, SparkSession


@dataclass
class JDBCConfig:
    url: str
    user: str
    password: str
    driver: str


def read(table: str, config: JDBCConfig) -> DataFrame:
    return (
        SparkSession.builder.getOrCreate()
        .read
        .option('driver', config.driver)
        .jdbc(
            url=config.url,
            table=table,
            properties={
                'user': config.user,
                'password': config.password,
            },
        )
    )
