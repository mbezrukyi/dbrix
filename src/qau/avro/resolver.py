from confluent_kafka.schema_registry import SchemaRegistryClient

from ..config import RegistryConfig


def build_registry(config: RegistryConfig) -> SchemaRegistryClient:
    return SchemaRegistryClient({
        'url': config.url,
        'basic.auth.user.info': config.auth,
    })


class SchemaResolver:
    def __init__(self, registry: SchemaRegistryClient):
        self._registry = registry

    def resolve(self, schema_id: str) -> str:
        return self._registry.get_schema(int(schema_id)).schema_str
