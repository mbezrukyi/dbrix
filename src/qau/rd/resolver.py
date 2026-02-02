from typing import Iterable

from confluent_kafka.schema_registry import SchemaRegistryClient


class SchemaResolver:
    def __init__(self, registry: SchemaRegistryClient):
        self._registry = registry

    def resolve(self, schemas: Iterable[str]) -> dict[str, str]:
        return {
            schema_id: self._registry.get_schema(schema_id).schema_str
            for schema_id in schemas
        }
