import csv
import json
from typing import Generator, List

from datalake import AtomType
from datalake.common.logger import logger


def split_list(list_to_split: list, slice_size: int) -> Generator[list, None, None]:
    for i in range(0, len(list_to_split), slice_size):
        yield list_to_split[i:i + slice_size]


def load_csv(file_name: str, delimiter: str = ',', column: int = 0) -> List[str]:
    """
    Load a CSV file and return one column in a list
    """
    ret = []
    i = 0  # Keep current row number in case of exception
    try:
        with open(file_name, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=delimiter)
            for i, row in enumerate(csv_reader):
                if row and not row[0].startswith('#'):  # We discard comments
                    ret.append(row[column])
    except IndexError:
        raise ValueError(f'Csv passed does not have enough columns on line {i} or the delimiter is incorrect')
    return ret


def load_list(file_name: str) -> list:
    """
    Load a file and retrieve each line in a list
    """
    return [line.rstrip('\n') for line in open(file_name)]


def split_input_file(input_file, n):
    """Yield successive n-sized chunks from the input file if it exceeds the limit (n)."""
    yield from split_list(load_list(input_file), n)


def save_output(file_name: str, data):
    """
    Save the data in a file.
    If data is dict, file format will be JSON.
    If data is a list, file format will be txt.
    Else it will be saved as it comes.
    """
    with open(file_name, 'w+') as file_to_write:
        if isinstance(data, dict):
            file_to_write.write(json.dumps(data, sort_keys=True, indent=2))
        elif isinstance(data, list):
            for item in data:
                file_to_write.write(f'{item}\n')
        else:
            file_to_write.write(data)


def parse_atom_type_or_exit(atom_type: str) -> AtomType:
    try:
        return AtomType[atom_type.upper()]
    except KeyError:
        logger.fatal(
            f'{atom_type} atom type is not supported, '
            f'use one of {[atom_type_.name.lower() for atom_type_ in AtomType]}'
        )
        exit(1)
