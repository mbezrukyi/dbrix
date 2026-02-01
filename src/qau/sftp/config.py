from dataclasses import dataclass


@dataclass
class Config:
    host: str
    username: str
    password: str
    port: int = 22

