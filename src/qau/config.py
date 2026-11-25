import dataclasses
from dataclasses import dataclass

from databricks.sdk import WorkspaceClient


@dataclass
class KafkaConfig:
    bootstrap: str
    jaas: str
    starting_offsets: str
    security_protocol: str
    sasl_mechanism: str


@dataclass
class RegistryConfig:
    url: str
    auth: str


def load[Config](config: type[Config], scope: str) -> Config:
    secrets = WorkspaceClient().dbutils.secrets
    stored_keys = {secret.key for secret in secrets.list(scope)}

    return config(**{
        field.name: field.type(secrets.get(scope, field.name))
        for field in dataclasses.fields(config)
        if field.name in stored_keys
    })
