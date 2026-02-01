from pyspark.sql import DataFrame

from ..config import KafkaConfig


class Writer:
    def __init__(self, config: KafkaConfig):
        self._config = config

    def write(self, df: DataFrame, topic: str) -> None:
        (
            df
            .write
            .format('kafka')
            .option('topic', topic)
            .option('kafka.bootstrap.servers', self._config.bootstrap)
            .option('kafka.security.protocol', self._config.security_protocol)
            .option('kafka.sasl.mechanism', self._config.sasl_mechanism)
            .option('kafka.sasl.jaas.config', self._config.jaas)
            .save()
        )
