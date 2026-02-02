from enum import Enum
from typing import Protocol

from pyspark.sql import DataFrame, SparkSession


class Env(Enum):
    DEV = 'tst'
    PROD = 'prd'
    QA = 'stg'


class Path:
    TEMPLATE = '/Volumes/{catalog}/artifacts/configs/mnt/{mount}/artifacts/qau/{file}'

    @classmethod
    def build(cls, env: Env, file: str) -> str:
        return cls.TEMPLATE.format(
            catalog=SparkSession.builder.getOrCreate().catalog.currentCatalog(),
            mount=f'{env.value}-configuration-realtime',
            file=file,
        )


class Reader(Protocol):
    def read(self) -> DataFrame:
        ...
