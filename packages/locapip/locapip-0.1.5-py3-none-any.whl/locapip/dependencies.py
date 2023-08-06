from locapip import name, __version__ as version
from typing import List
from fastapi import WebSocket
import pydantic
import pathlib
import os


class AppConfig:
    def __init__(self):
        self.name = name
        self.version = version
        self.data_root_dir: pathlib.Path = pathlib.Path()
        self.host: str = "127.0.0.1"
        self.port: int = 6547

        readme = pathlib.Path(os.path.dirname(__file__)) / "README.md"
        with open(readme, "r", encoding="UTF-8") as f:
            self.description = f.read()

    def is_valid_path(self, path):
        return str(self.data_root_dir.resolve()) in str(path.resolve())


app_config = AppConfig()


class Detail(pydantic.BaseModel):
    completed: bool = True
    detail: str = ""

    def set(self, completed: bool, detail: str):
        self.completed = completed
        self.detail = detail
        return self
