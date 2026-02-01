from pyspark.sql import DataFrame

from .parser import Parser
from .reader import Reader
from .writer import Writer


class KafkaSource:
    def __init__(self, reader: Reader, parser: Parser):
        self._reader = reader
        self._parser = parser

    def load(self, topic: str) -> DataFrame:
        return self._parser.from_(self._reader.read(topic))


class KafkaSink:
    def __init__(self, writer: Writer, parser: Parser):
        self._writer = writer
        self._parser = parser

    def upload(self, df: DataFrame, topic: str) -> None:
        self._writer.write(self._parser.to(df), topic)

