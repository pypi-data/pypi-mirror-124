import argparse

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
