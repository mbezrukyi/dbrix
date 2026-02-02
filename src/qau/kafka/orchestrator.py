from pyspark.sql import DataFrame

from .parser import KafkaParser
from .reader import KafkaReader
from .writer import KafkaWriter


class KafkaSource:
    def __init__(self, reader: KafkaReader, parser: KafkaParser):
        self._reader = reader
        self._parser = parser

    def load(self) -> DataFrame:
        return self._parser.from_(self._reader.read())


class KafkaSink:
    def __init__(self, writer: KafkaWriter, parser: KafkaParser):
        self._writer = writer
        self._parser = parser

    def upload(self, df: DataFrame) -> None:
        self._writer.write(self._parser.to(df))
