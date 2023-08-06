from pathlib import Path
from urllib.parse import urlparse

import typer

from .parser import generate_code

app = typer.Typer(
    no_args_is_help=True,
    invoke_without_command=True,
    add_completion=False,
)

state = {"verbose": False}


@app.command('generate')
def gen(
        url: str,
        output_dir: Path = typer.Option(
            ...,
            "-o",
            "--output-dir",
            dir_okay=True,
            file_okay=False,
            writable=True,
            resolve_path=True,
            help="directory for generated models and client instance"
        ),
        authorization_header: str = typer.Option(
            None,
            "-a",
            "--auth",
            "--authorization-header",
        )
):
    """
    Generate client from specified url
    """
    typer.echo(f"Generating OpenAPI client from {url}")
    typer.echo(f"All files will be saved to {output_dir}")
    generate_code(
        str(urlparse(url).geturl()),
        output_dir,
        authorization_header=authorization_header
    )


@app.callback()
def main(ctx: typer.Context):
    """
    Generates OpenAPI http client based on httpx library from OpenAPI schema
    """
