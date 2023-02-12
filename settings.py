from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
        These settings can be overwritten with env vars on uppercase

        Example: mongodb_url is replaced by the MONGODB_URL env var
    """
    yolo_labels_filename = ""
    yolo_config_filename = ""
    yolo_weights_filename = ""


@lru_cache
def settings():
    return Settings(_env_file='.env', _env_file_encoding='utf-8')
