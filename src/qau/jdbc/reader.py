from pyspark.sql import DataFrame, SparkSession

from .config import JDBCConfig


class JDBCReader:
    def __init__(self, config: JDBCConfig):
        self._config = config

    def read(self, table: str) -> DataFrame:
        return (
            SparkSession.builder.getOrCreate()
            .read
            .option('driver', self._config.driver)
            .jdbc(
                url=self._config.url,
                table=table,
                properties={
                    'user': self._config.user,
                    'password': self._config.password,
                }
            )
        )
