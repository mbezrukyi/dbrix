from typing import ClassVar

from confluent_kafka.schema_registry import SchemaRegistryClient


class KafkaConfig:
    FILE: ClassVar[str] = 'kafka.ini'

    def __init__(
        self,
        bootstrap: str,
        jaas: str,
        starting_offsets: str,
        security_protocol: str,
        sasl_mechanism: str,
    ):
        self.bootstrap = bootstrap
        self.jaas = jaas
        self.starting_offsets = starting_offsets
        self.security_protocol = security_protocol
        self.sasl_mechanism = sasl_mechanism


class RegistryConfig:
    FILE: ClassVar[str] = 'registry.ini'

    def __init__(self, url: str, auth: str):
        self.url = url
        self.auth = auth

    def create(self) -> SchemaRegistryClient:
        return SchemaRegistryClient({
            'url': self.url,
            'basic.auth.user.info': self.auth,
        })
