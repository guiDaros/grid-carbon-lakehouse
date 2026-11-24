"""Command-line entry point: `gridcarbon <command>`.

All pipeline logic is exposed here; orchestrators only call these commands.
"""

from typing import Annotated

import typer

from gridcarbon import __version__

app = typer.Typer(
    name="gridcarbon",
    help="Grid Carbon Lakehouse command-line interface.",
    no_args_is_help=True,
    add_completion=False,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"gridcarbon {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Show the version and exit.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Grid Carbon Lakehouse command-line interface."""
