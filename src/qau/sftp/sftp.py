from .connector import SFTPConnector


class SFTP:
    def __init__(self, connector: SFTPConnector):
        self._connector = connector

    def extract(self, path: str) -> list[str]:
        with self._connector as sftp:
            return sftp.listdir(path)

    def read(self, path: str) -> str:
        with self._connector as sftp:
            with sftp.open(path) as file:
                return file.readlines()

    def upload(self, local: str, remote: str) -> None:
        with self._connector as sftp:
            sftp.put(local, remote)

    def load(self, remote: str, local: str) -> None:
        with self._connector as sftp:
            sftp.get(remote, local)

    def delete(self, path: str) -> None:
        with self._connector as sftp:
            sftp.remove(path)

    def move(self, old: str, new: str) -> None:
        with self._connector as sftp:
            sftp.rename(old, new)
