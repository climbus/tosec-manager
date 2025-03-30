from itertools import groupby
from parser import TosecFile
from typing import Callable, Sequence


def _choose_best_file(
    files: Sequence[TosecFile], formats: Sequence[str], languages: Sequence[str]
) -> TosecFile:
    return sorted(
        files,
        key=lambda x: (
            (formats.index(x.extension) if x.extension in formats else len(formats)),
            (
                languages.index(x.language)
                if x.language in languages
                else len(languages)
            ),
            len(x.flags),
        ),
    )[0]


def get_bestchoice_filter(
    formats: Sequence[str] = [], languages: Sequence[str] = []
) -> Callable[[Sequence[TosecFile]], Sequence[TosecFile]]:

    def bestchoice(lst: Sequence[TosecFile]) -> Sequence[TosecFile]:
        result: Sequence[TosecFile] = []

        lst_sorted = sorted(lst, key=lambda x: (x.title.upper(), x.publisher.upper()))

        for _, group in groupby(lst_sorted, lambda x: (x.title, x.publisher)):
            result.append(_choose_best_file(list(group), formats, languages))

        return result

    return bestchoice
