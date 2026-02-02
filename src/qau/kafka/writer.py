from pyspark.sql import DataFrame

from ..config import KafkaConfig


class KafkaWriter:
    def __init__(self, topic: str, config: KafkaConfig):
        self.topic = topic

        self._config = config

    def write(self, df: DataFrame) -> None:
        (
            df
            .write
            .format('kafka')
            .option('topic', self.topic)
            .option('kafka.bootstrap.servers', self._config.bootstrap)
            .option('kafka.security.protocol', self._config.security_protocol)
            .option('kafka.sasl.mechanism', self._config.sasl_mechanism)
            .option('kafka.sasl.jaas.config', self._config.jaas)
            .save()
        )
