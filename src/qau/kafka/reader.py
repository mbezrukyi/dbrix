from pyspark.sql import DataFrame, SparkSession

from ..config import KafkaConfig


class KafkaReader:
    def __init__(self, topic: str, config: KafkaConfig):
        self.topic = topic

        self._config = config

    def read(self) -> DataFrame:
        return (
            SparkSession.builder.getOrCreate()
            .read
            .format('kafka')
            .option('kafka.bootstrap.servers', self._config.bootstrap)
            .option('subscribe', self.topic)
            .option('startingOffsets', self._config.starting_offsets)
            .option('kafka.security.protocol', self._config.security_protocol)
            .option('kafka.sasl.mechanism', self._config.sasl_mechanism)
            .option('kafka.sasl.jaas.config', self._config.jaas)
            .load()
        )
