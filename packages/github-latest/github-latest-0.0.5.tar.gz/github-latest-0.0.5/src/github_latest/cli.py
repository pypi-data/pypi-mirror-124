"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mgithub_latest` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``github_latest.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``github_latest.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import argparse
import logging
import pathlib
import re
import sys

import monacelli_pylog_prefs.logger
import requests


def main(argv=sys.argv):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Does stuff.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "url", help="example https://github.com/mozilla/sops/releases/latest"
    )

    parser.add_argument(
        "-l",
        "--log",
        dest="logLevel",
        default="INFO",
        choices=[
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
            "debug",
            "info",
            "warning",
            "error",
            "critical",
        ],
        help="Set the logging level",
    )

    args = parser.parse_args()

    monacelli_pylog_prefs.logger.setup(stream_level=args.logLevel.upper())

    response = requests.get(args.url)
    path = pathlib.Path(response.url)
    tag = path.name
    version = tag.replace("v", "")

    try:
        re.search(r"([\d.]+)", version).group(1)
    except AttributeError as ex:
        logging.exception(f"{args.url} has no releases")
        raise

    logging.debug(f"{response.url=}")
    logging.debug(f"{tag=}")
    logging.debug(f"{version=}")
    print(f"{version}")
    return 0
