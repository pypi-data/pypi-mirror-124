from itertools import groupby
from typing import List

from .._io import read_ints_from_csv
from ..logger import admin_logger
from ..utils import as_range, groupby_range


def _read_userids(filename: str) -> List[int]:
    return read_ints_from_csv(filename, "uid")


def _read_groupids(filename: str) -> List[int]:
    return read_ints_from_csv(filename, "gid")


def main(users_file: str, group_file: str) -> None:
    """
    Prints the used ID ranges for all groups and users.
    """
    userids = _read_userids(users_file)
    groupids = _read_groupids(group_file)

    uid_ranges = ",".join(as_range(g) for _, g in groupby(userids, groupby_range))
    gid_ranges = ",".join(as_range(g) for _, g in groupby(groupids, groupby_range))

    admin_logger.info(f"Used UID ranges: {uid_ranges}")
    admin_logger.info(f"Used GID ranges: {gid_ranges}")
