import os

CFMID_PATH = "CFMID_PATH"
CFMID_IMAGE = "CFMID_IMAGE"


class ConfigError(Exception):
    pass


class Config:
    def get(self, key: str) -> str:
        try:
            return os.environ[key]
        except KeyError as exc:
            raise ConfigError(f"Missing {key} environment variable") from exc


config = Config()
