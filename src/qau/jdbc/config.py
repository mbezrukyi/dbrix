from dataclasses import dataclass


@dataclass
class JDBCConfig:
    url: str
    user: str
    password: str
    driver: str
