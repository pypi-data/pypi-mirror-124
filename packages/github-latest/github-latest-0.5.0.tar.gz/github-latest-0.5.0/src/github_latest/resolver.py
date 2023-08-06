import abc
import dataclasses
import json
import logging
import pathlib
import re

import requests


class ResolverStrategy(abc.ABC):

    def get(self, url: str) -> requests.Response:
        response = requests.get(url)
        assert response.status_code == 200
        return response

    @abc.abstractmethod
    def resolve(self):
        pass


class ApiResolvingStragey(ResolverStrategy):

    def change_endpoint(self, url: str) -> str:
        api = url.replace("https://github.com", "https://api.github.com/repos")
        logging.debug(f"{api=}")
        return api

    def resolve(self, url: str) -> str:

        url = self.change_endpoint(url)
        response = self.get(url)

        js = response.json()
        logging.debug(json.dumps(js, indent=2))

        tag = js.get("tag_name")
        logging.debug(f"{tag=}")

        version = tag.replace("v", "")
        logging.debug(f"{version=}")

        return version


class RedirectResolvingStragey(ResolverStrategy):

    def resolve(self, url: str) -> str:
        response = self.get(url)

        logging.debug(f"{response.url=}")

        path = pathlib.Path(response.url)
        logging.debug(f"{path=}")
        logging.debug(f"{path.name=}")

        version = path.name.replace("v", "")
        logging.debug(f"{version=}")

        return version


@dataclasses.dataclass
class Resolver:
    url: str
    resolver: ResolverStrategy
    version: str = None

    def __post_init__(self):
        logging.debug(f"{self.url=}")

    def resolve(self):
        self.version = self.resolver.resolve(self.url)

    def version_found(self):
        if re.search(r"([\d.]+)", self.version):
            return True
        return False
