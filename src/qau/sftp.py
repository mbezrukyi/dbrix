from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

import paramiko


@dataclass
class SFTPConfig:
    host: str
    username: str
    password: str
    port: int = 22


@contextmanager
def connect(config: SFTPConfig) -> Iterator[paramiko.SFTPClient]:
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=config.host,
            port=config.port,
            username=config.username,
            password=config.password,
        )

        with client.open_sftp() as sftp:
            yield sftp
