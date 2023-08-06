import argparse as _argparse
import getpass as _getpass
import logging as _logging
import typing as _typing

__version__ = "2.1.1"
__author__ = "Carneiro, Claudio F."
__date__ = "Mon, 25 Oct 2021 15:29:23 +0000"


def get_logger(
    name=__file__,
    level: int = _logging.WARNING,
    handlers: _typing.Optional[_typing.List[_logging.Handler]] = None,
) -> _logging.Logger:
    """Returns a logger object"""

    logger = _logging.getLogger(name)

    if not len(logger.handlers) and not handlers:
        formatter = _logging.Formatter(
            "[%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(funcName)s] %(message)s"
        )
        logger.setLevel(level)
        console = _logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    return logger


class PasswordPromptAction(_argparse.Action):
    """Custom password prompt action
    usage:

    >> parser = argparse.ArgumentParser(
        "Initialize a Taiga Project, ENG spreadsheet integration.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    >> parser.add_argument("-u", "--user", dest="user", type=str, required=True)
    >> parser.add_argument("-p", "--password", dest="password", action=PasswordPromptAction, type=str, required=True)

    >> args = parser.parse_args()"""

    def __init__(
        self,
        option_strings,
        dest=None,
        nargs=0,
        default=None,
        required=False,
        type=None,
        metavar=None,
        help=None,
    ):
        super(PasswordPromptAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            default=default,
            required=required,
            metavar=metavar,
            type=type,
            help=help,
        )

    def __call__(self, parser, args, values, option_string=None):
        password = _getpass.getpass()
        setattr(args, self.dest, password)
