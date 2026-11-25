from dataclasses import dataclass

from pyspark.sql import DataFrame, SparkSession


@dataclass
class KafkaConfig:
    bootstrap: str
    jaas: str
    security_protocol: str
    sasl_mechanism: str


def read(
    topic: str,
    config: KafkaConfig,
    starting_offsets: str = 'earliest',
) -> DataFrame:
    return (
        SparkSession.builder.getOrCreate()
        .read
        .format('kafka')
        .options(**_connection_options(config))
        .option('subscribe', topic)
        .option('startingOffsets', starting_offsets)
        .load()
    )


def write(df: DataFrame, topic: str, config: KafkaConfig) -> None:
    (
        df
        .write
        .format('kafka')
        .options(**_connection_options(config))
        .option('topic', topic)
        .save()
    )


def _connection_options(config: KafkaConfig) -> dict[str, str]:
    return {
        'kafka.bootstrap.servers': config.bootstrap,
        'kafka.security.protocol': config.security_protocol,
        'kafka.sasl.mechanism': config.sasl_mechanism,
        'kafka.sasl.jaas.config': config.jaas,
    }
