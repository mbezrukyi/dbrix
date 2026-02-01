import configparser

from .common import Env, Path, T


class Loader:
    def __init__(self, env: Env):
        self.env = env

    def load(self, config: type[T]) -> T:
        parser = configparser.ConfigParser()

        parser.read(Path.build(self.env, config.FILE))

        return config(**parser[self.env.value])

