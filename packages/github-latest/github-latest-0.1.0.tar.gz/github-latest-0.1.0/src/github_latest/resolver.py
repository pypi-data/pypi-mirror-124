import dataclasses
import logging
import pathlib
import re

import requests


@dataclasses.dataclass
class Resolver:
    url: str
    version: str = None

    def __post_init__(self):
        logging.debug(f"{self.url=}")

    def resolve(self) -> str:
        response = requests.get(self.url)
        logging.debug(f"{response.url=}")

        path = pathlib.Path(response.url)
        logging.debug(f"{path=}")
        logging.debug(f"{path.name=}")

        self.version = path.name.replace("v", "")
        logging.debug(f"{self.version=}")

    def version_found(self):
        if re.search(r"([\d.]+)", self.version):
            return True
        return False
