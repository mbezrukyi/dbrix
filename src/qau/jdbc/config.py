from dataclasses import dataclass


@dataclass
class Config:
    url: str
    user: str
    password: str
    driver: str

