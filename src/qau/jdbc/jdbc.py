from pyspark.sql import DataFrame, SparkSession

from .config import Config


class JDBC:
    def __init__(self, config: Config):
        self._config = config

    def extract(self, table: str) -> DataFrame:
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

