import string
from itertools import groupby

ALPHABET = string.ascii_uppercase
ALPHABET_LEN = len(ALPHABET)

from logging import getLogger
from parser import TosecFile
from typing import Dict, List, Optional, Protocol, Sequence

logger = getLogger(__name__)


def _is_number_or_special(char: str) -> bool:
    return char.isdigit() or not char.isalnum()


def _create_dir_name(
    dirname: str, start: int, end: int, include_special: bool = False
) -> str:
    """Create a directory name based on the start and end indices."""
    if _is_number_or_special(dirname):
        return "#"

    if include_special:
        return f"{dirname}#-{dirname}{ALPHABET[end]}"

    return f"{dirname}{ALPHABET[start]}-{dirname}{ALPHABET[end]}"


def _has_to_limit(dir_limit: Optional[int], group_len: int) -> bool:
    return bool(dir_limit and group_len > dir_limit)


def _compute_end_index(i: int, letters_in_dir: int) -> int:
    end = i * letters_in_dir + letters_in_dir - 1
    return end


def _exceeds_limit(dir_limit: int, start: int, end: int, elms: List[TosecFile]) -> bool:
    """Check if the number of elements in the range exceeds the directory limit."""

    return (
        sum(
            1
            for elm in elms
            if len(elm.title) > 1 and elm.title[1].upper() in ALPHABET[start : end + 1]
        )
        > dir_limit
    )


def _prepare_dirs(
    lst: Sequence[TosecFile], dir_limit: Optional[int]
) -> Dict[str, List[TosecFile]]:
    result: Dict[str, List[TosecFile]] = {}
    lst_sorted = sorted(lst, key=lambda x: x.title.upper())

    for letter, grouped in groupby(lst_sorted, lambda x: x.first_letter):
        logger.info(f"Grouping by {letter}")

        elms = list(grouped)
        group_len = len(elms)

        if not _has_to_limit(dir_limit, group_len):
            dirname = "#" if _is_number_or_special(letter) else letter
            result.setdefault(dirname, [])

            logger.info(f"Adding {group_len} items to {dirname}")
            continue

        # assrtion for typing purposes
        assert dir_limit is not None

        logger.info(f"Splitting {group_len} items into directories")

        dirs_count = group_len // dir_limit

        if group_len % dir_limit != 0:
            dirs_count += 1

        if dirs_count > ALPHABET_LEN:
            dirs_count = ALPHABET_LEN

        letters_in_dir = ALPHABET_LEN // dirs_count

        start_index = 0
        for i in range(dirs_count):
            end_index = _compute_end_index(i, letters_in_dir)
            end_index = _find_best_count(dir_limit, start_index, end_index, elms)

            include_special = i == 0
            dir_name = _create_dir_name(letter, start_index, end_index, include_special)
            result.setdefault(dir_name, [])

            start_index = end_index + 1
    return result


def _find_best_count(
    dir_limit: int, start_index: int, end_index: int, elms: List[TosecFile]
) -> int:
    while True:
        if not _exceeds_limit(dir_limit, start_index, end_index, elms):
            break
        logger.debug(
            f"Reducing end index from {end_index} to {end_index - 1} length: {len(elms)}"
        )
        end_index -= 1
    return end_index


class GroupBy(Protocol):
    def __call__(
        self, lst: Sequence[TosecFile], dir_limit: Optional[int] = None
    ) -> Dict[str, List[TosecFile]]: ...


def place_item_in_dir(
    item: TosecFile, dirs: Dict[str, List[TosecFile]]
) -> Dict[str, List[TosecFile]]:
    first_char = item.title[0].upper()
    for dir_name in dirs.keys():
        if "-" in dir_name:
            start, end = [name[1] for name in dir_name.split("-")]
            if (
                len(item.title) > 1
                and item.title[0].upper() == dir_name[0]
                and start <= item.title[1].upper() <= end
            ):
                dirs[dir_name].append(item)
                break
            if (
                start == "#"
                and item.title[0].upper() == dir_name[0]
                and len(item.title) > 1
                and _is_number_or_special(item.title[1])
            ):
                dirs[dir_name].append(item)
                break
        elif dir_name == first_char or (
            dir_name == "#" and _is_number_or_special(first_char)
        ):
            dirs[dir_name].append(item)
            break
    return dirs


def get_group_by() -> GroupBy:
    def group_by(
        lst: Sequence[TosecFile], dir_limit: Optional[int] = None
    ) -> Dict[str, List[TosecFile]]:

        dirs = _prepare_dirs(lst, dir_limit)

        for item in lst:
            place_item_in_dir(item, dirs)
        return dirs

    return group_by
