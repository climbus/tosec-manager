import string
from itertools import groupby
from parser import TosecFile
from typing import Dict, List, Optional, Protocol, Sequence


def _is_number_or_special(char: str) -> bool:
    return char.isdigit() or not char.isalnum()


def _prepare_dirs(
    lst: Sequence[TosecFile], dir_limit: Optional[int]
) -> Dict[str, List[TosecFile]]:
    result: Dict[str, List[TosecFile]] = {}

    for dirname, elms in groupby(lst, lambda x: x.title[0].upper()):
        group_len = len(list(elms))
        if dir_limit and group_len > dir_limit:
            parts = group_len // dir_limit
            letters_in_dir = len(string.ascii_uppercase) // parts
            for i in range(parts):
                start = i * letters_in_dir
                end = i * letters_in_dir + letters_in_dir - 1
                result.setdefault(
                    f"{dirname}{string.ascii_uppercase[start]}-{dirname}{string.ascii_uppercase[end]}",
                    [],
                )
        else:
            result.setdefault("#" if _is_number_or_special(dirname) else dirname, [])

    return result


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
            if start <= item.title[1].upper() <= end:
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
