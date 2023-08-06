import typer

from ..logger import user_logger

app = typer.Typer(help="Various benchmarks for DICE")


@app.command()
def run_hepspec06() -> None:
    """Run the hepspec06 benchmark"""
    user_logger.warning("Not implemented yet")
