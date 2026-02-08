#!/usr/bin/env python3
from __future__ import annotations

import typer

from ._version import __version__
from .mirror_data import apt_sources, yum_repos
from .os_info import detect_os
from .sources import set_apt_sources, set_yum_repos

app = typer.Typer()


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"mirror-man version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the application's version and exit.",
    ),
) -> None:
    """A command-line tool to manage mirror sources."""


@app.command()
def aliyun() -> None:
    """Switch to Aliyun mirror sources."""
    os_info = detect_os()
    mirror_key = os_info.mirror_key

    if os_info.id == "ubuntu":
        if mirror_key not in apt_sources:
            typer.echo(f"Aliyun mirror source not found for {os_info.pretty_name}.")
            raise typer.Exit(code=1)
        try:
            set_apt_sources(apt_sources[mirror_key])
            typer.echo(f"Successfully switched to Aliyun mirror for {os_info.pretty_name}.")
        except Exception as e:
            typer.echo(f"Failed to switch to Aliyun mirror for {os_info.pretty_name}: {e}")
            raise typer.Exit(code=1)

    elif os_info.id == "centos":
        if mirror_key not in yum_repos:
            typer.echo(f"Aliyun mirror source not found for {os_info.pretty_name}.")
            raise typer.Exit(code=1)
        repos = yum_repos[mirror_key]
        try:
            set_yum_repos(repos["base"], repos["epel"])
            typer.echo(f"Successfully switched to Aliyun mirror for {os_info.pretty_name}.")
        except Exception as e:
            typer.echo(f"Failed to switch to Aliyun mirror for {os_info.pretty_name}: {e}")
            raise typer.Exit(code=1)

    else:
        typer.echo(f"Unsupported operating system: {os_info.pretty_name}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
