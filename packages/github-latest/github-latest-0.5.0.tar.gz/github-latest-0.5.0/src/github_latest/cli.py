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

import sys

import monacelli_pylog_prefs.logger

import github_latest.args
from github_latest.resolver import ApiResolvingStragey
from github_latest.resolver import RedirectResolvingStragey
from github_latest.resolver import Resolver

def main(argv=sys.argv):
    monacelli_pylog_prefs.logger.setup(
        stream_level=github_latest.args.args.logLevel.upper()
    )

    strategy = ApiResolvingStragey()
    strategy = RedirectResolvingStragey()

    resolver = Resolver(github_latest.args.args.url, strategy)
    resolver.resolve()
    print(f"{resolver.version}")

    if not resolver.version_found():
        return 1
    return 0
