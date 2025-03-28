from collections.abc import Callable
from parser import TosecFile
from typing import Dict, List, Sequence


def _is_number_or_special(char: str) -> bool:
    return char.isdigit() or not char.isalnum()


def get_group_by() -> Callable[[Sequence[TosecFile], int], Dict[str, List[TosecFile]]]:
    def group_by(
        lst: Sequence[TosecFile], dir_limit: int
    ) -> Dict[str, List[TosecFile]]:
        result: Dict[str, List[TosecFile]] = {}

        if dir_limit:
            dirs = len(lst) // dir_limit

        for item in lst:
            result.setdefault(
                "#" if _is_number_or_special(item.title[0]) else item.title[0].upper(),
                [],
            ).append(item)

        return result

    return group_by
