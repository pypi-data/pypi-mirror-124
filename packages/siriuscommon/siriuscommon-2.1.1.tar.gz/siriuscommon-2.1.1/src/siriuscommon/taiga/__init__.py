import argparse as _argparse

from .. import PasswordPromptAction, get_logger
from .client import TaigaClient, _taiga_default_url

logger = get_logger("Taiga")


def taiga_export_xlsx():
    parser = _argparse.ArgumentParser(
        "Export a Taiga Project for ENG spreadsheet integration.",
        formatter_class=_argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--slug",
        help=f"Project slug, the text located on your project URL. e.g.: {_taiga_default_url}/project/<project_slug> ",
        default="grupo-automacao-e-software",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        help="Output filename",
        default="user-stories.xlsx",
        required=False,
    )
    parser.add_argument(
        "--url", help="Taiga base URL", default=_taiga_default_url, required=False
    )
    parser.add_argument(
        "-u",
        "--username",
        dest="username",
        required=True,
        help="Taiga username with the required permissions.",
    )
    parser.add_argument(
        "-p",
        "--password",
        dest="password",
        action=PasswordPromptAction,
        type=str,
        required=True,
    )

    args = parser.parse_args()
    client = TaigaClient(host=args.url)
    logger.info("Authenticating...")
    client.auth(args.username, args.password)
    logger.info("Reading CSV...")
    df = client.get_stories_df(slug=args.slug)
    logger.info(f"Exporting to '{args.output}'")
    client.to_excel_table(df, filename=args.output)


def taiga_initialize_project():
    parser = _argparse.ArgumentParser(
        "Initialize a Taiga Project, ENG spreadsheet integration.",
        formatter_class=_argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--slug",
        help=f"Project slug, the text located on your project URL. e.g.: {_taiga_default_url}/project/<project_slug> ",
        default="grupo-automacao-e-software",
    )
    parser.add_argument(
        "--url", help="Taiga base URL", default=_taiga_default_url, required=False
    )
    parser.add_argument(
        "-u",
        "--username",
        dest="username",
        required=True,
        help="Taiga username with the required permissions.",
    )
    parser.add_argument(
        "-p",
        "--password",
        dest="password",
        action=PasswordPromptAction,
        type=str,
        required=True,
    )

    args = parser.parse_args()

    client = TaigaClient(host=args.url)

    logger.info("Authenticating...")
    client.auth(args.username, args.password)

    logger.info("Initialising project")
    client.initialize_project(slug=args.slug)
