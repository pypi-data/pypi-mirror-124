import logging

from rich.logging import RichHandler

from .utils import current_date, current_linux_user


class VariableFormatter(logging.Formatter):
    """
    From https://stackoverflow.com/q/14844970
    Formatter that allows for different formatting of the message
    depending on the log level.
    """

    err_fmt = "%(levelname)s: %(message)s"
    warn_fmt = "%(levelname)s: %(message)s"
    info_fmt = "%(message)s"
    dbg_fmt = "%(asctime)s [%(name)s]  %(levelname)s: %(message)s"

    def __init__(self, fmt: str = "%(levelno)s: %(msg)s") -> None:
        super().__init__(fmt=fmt, datefmt=None, style="%")

    def format(self, record: logging.LogRecord) -> str:

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._style._fmt = VariableFormatter.dbg_fmt

        elif record.levelno == logging.INFO:
            self._style._fmt = VariableFormatter.info_fmt

        elif record.levelno == logging.ERROR:
            self._style._fmt = VariableFormatter.err_fmt

        elif record.levelno == logging.WARNING:
            self._style._fmt = VariableFormatter.warn_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result


admin_logger = logging.getLogger("dice_admin")
admin_logger.setLevel(logging.INFO)

user_logger = logging.getLogger("dice_user")
user_logger.setLevel(logging.INFO)

console_formatter = VariableFormatter()
console_handler = RichHandler(rich_tracebacks=True, markup=True)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formatter)

logfile_formatter = logging.Formatter(
    "%(asctime)s [%(name)s]  %(levelname)s: %(message)s"
)
logfile_handler = logging.FileHandler(
    f"/tmp/dice_commands_{current_linux_user()}_{current_date()}.log"
)
logfile_handler.setLevel(logging.DEBUG)
logfile_handler.setFormatter(logfile_formatter)

admin_logger.addHandler(console_handler)
admin_logger.addHandler(logfile_handler)

user_logger.addHandler(console_handler)
user_logger.addHandler(logfile_handler)
