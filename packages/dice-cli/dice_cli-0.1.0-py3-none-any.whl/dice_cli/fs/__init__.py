import typer

from ..logger import user_logger

app = typer.Typer(help="DICE filesystem commands")


@app.command()
def copy_from_local(
    src: str = typer.Argument(..., help="Source path"),
    dst: str = typer.Argument(..., help="Destination path"),
) -> None:
    """
    Copy a file from local to DICE.

    Parameters
    ----------
    src : str
        Source path.
    dst : str
        Destination path.
    """
    user_logger.info(f"Copying file from local to DICE: {src} -> {dst}")
    user_logger.warning("Not implemented yet")
