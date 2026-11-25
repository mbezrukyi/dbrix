import dataclasses

from databricks.sdk import WorkspaceClient


def load[Config](config: type[Config], scope: str) -> Config:
    secrets = WorkspaceClient().dbutils.secrets
    stored_keys = {secret.key for secret in secrets.list(scope)}

    return config(**{
        field.name: field.type(secrets.get(scope, field.name))
        for field in dataclasses.fields(config)
        if field.name in stored_keys
    })
