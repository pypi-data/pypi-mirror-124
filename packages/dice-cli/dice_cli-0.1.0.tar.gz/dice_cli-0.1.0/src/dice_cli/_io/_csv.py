import csv
from typing import Any, Dict, List


def read_ints_from_csv(filename: str, fieldname: str) -> List[int]:
    """
    Reads data from CSV file and converts {fieldname} to int.
    Returned data is sorted
    """
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter=",", quotechar='"')
        data = [int(row[fieldname]) for row in reader]
        data.sort()
    return data


def write_list_data_as_dict_to_csv(
    data: List[Dict[str, Any]], output_file: str, fieldnames: List[str]
) -> None:
    with open(output_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
