import paramiko
import paramiko.sftp_client

from .config import SFTPConfig


class SFTPConnector:
    def __init__(self, config: SFTPConfig):
        self._config = config
        self._client = paramiko.SSHClient()
        self._sftp = None

    def __enter__(self):
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.connect(
            hostname=self._config.host,
            port=self._config.port,
            username=self._config.username,
            password=self._config.password,
        )

        self._sftp = self._client.open_sftp()

        return self._sftp

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._sftp.close()
        self._client.close()
