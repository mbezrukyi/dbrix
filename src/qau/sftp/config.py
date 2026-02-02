from dataclasses import dataclass


@dataclass
class SFTPConfig:
    host: str
    username: str
    password: str
    port: int = 22
