import typer

from . import _print_unused_id_ranges, _print_used_id_ranges, _scan_groups_and_users

app = typer.Typer(help="DICE admin commands")


@app.command()
def scan_groups_and_users() -> None:
    _scan_groups_and_users.main()


@app.command()
def print_used_id_ranges(
    user_file: str = typer.Argument(..., help="CSV file containing users"),
    group_file: str = typer.Argument(..., help="CSV file containing groups"),
) -> None:
    _print_used_id_ranges.main(user_file, group_file)


@app.command()
def print_unused_id_ranges(
    user_file: str = typer.Argument(..., help="CSV file containing users"),
    group_file: str = typer.Argument(..., help="CSV file containing groups"),
) -> None:
    _print_unused_id_ranges.main(user_file, group_file)
