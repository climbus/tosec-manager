import string
from itertools import groupby
from parser import TosecFile
from typing import Dict, List, Optional, Protocol, Sequence


def _is_number_or_special(char: str) -> bool:
    return char.isdigit() or not char.isalnum()


def _create_dir_name(dirname: str, start: int, end: int) -> str:
    """Create a directory name based on the start and end indices."""
    if _is_number_or_special(dirname):
        return "#"
    return f"{dirname}{string.ascii_uppercase[start]}-{dirname}{string.ascii_uppercase[end]}"


def _has_to_limit(dir_limit: Optional[int], group_len: int) -> bool:
    return bool(dir_limit and group_len > dir_limit)


def _compute_bounds(i: int, letters_in_dir: int) -> tuple[int, int]:
    start = i * letters_in_dir
    end = i * letters_in_dir + letters_in_dir - 1
    return start, end


def _prepare_dirs(
    lst: Sequence[TosecFile], dir_limit: Optional[int]
) -> Dict[str, List[TosecFile]]:
    result: Dict[str, List[TosecFile]] = {}
    lst_sorted = sorted(lst, key=lambda x: x.title)

    for dirname, elms in groupby(lst_sorted, lambda x: x.title[0].upper()):
        print(dirname)
        group_len = len(list(elms))

        if not _has_to_limit(dir_limit, group_len):
            dir_name = "#" if _is_number_or_special(dirname) else dirname
            result.setdefault(dir_name, [])
            continue

        assert dir_limit is not None

        parts = group_len // dir_limit
        letters_in_dir = len(string.ascii_uppercase) // parts

        for i in range(parts):
            start, end = _compute_bounds(i, letters_in_dir)
            dir_name = _create_dir_name(dirname, start, end)
            result.setdefault(dir_name, [])

    return result


class GroupBy(Protocol):
    def __call__(
        self, lst: Sequence[TosecFile], dir_limit: Optional[int] = None
    ) -> Dict[str, List[TosecFile]]: ...


def place_item_in_dir(
    item: TosecFile, dirs: Dict[str, List[TosecFile]]
) -> Dict[str, List[TosecFile]]:
    first_char = item.title[0].upper()
    print(dirs.keys())
    for dir_name in dirs.keys():
        print(dir_name, first_char)
        if "-" in dir_name:
            start, end = [name[1] for name in dir_name.split("-")]
            print(start, end, dir_name)
            if (
                len(item.title) > 1
                and item.title[0].upper() == dir_name[0]
                and start <= item.title[1].upper() <= end
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
        print(dirs)

        for item in lst:
            place_item_in_dir(item, dirs)
        return dirs

    return group_by
