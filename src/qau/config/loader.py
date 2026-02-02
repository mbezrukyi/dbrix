import configparser

from .config import T
from ..common import Env, Path


class ConfigLoader:
    def __init__(self, env: Env):
        self.env = env

    def load(self, config: type[T]) -> T:
        parser = configparser.ConfigParser()

        parser.read(Path.build(self.env, config.FILE))

        return config(**parser[self.env.value])
