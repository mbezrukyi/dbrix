from enum import Enum
from typing import Any, ClassVar, Protocol, TypeVar

from pyspark.sql import SparkSession


T = TypeVar('T', bound='Config')


class Env(Enum):
    DEV = 'tst'
    PROD = 'prd'
    QA = 'stg'


class Config(Protocol):
    FILE: ClassVar[str]

    def __init__(self, **kwargs: Any):
        ...


class Path:
    TEMPLATE = '/Volumes/{catalog}/artifacts/configs/mnt/{mount}/artifacts/qau/{file}'

    @classmethod
    def build(cls, env: Env, file: str) -> str:
        return cls.TEMPLATE.format(
            catalog=SparkSession.builder.getOrCreate().catalog.currentCatalog(),
            mount=f'{env.value}-configuration-realtime',
            file=file,
        )

