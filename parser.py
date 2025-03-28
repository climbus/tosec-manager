import re
from dataclasses import dataclass as datasclass
from enum import Enum
from logging import getLogger
from typing import List, Tuple

logger = getLogger(__name__)


class FLAG(Enum):
    ALTERNATE_VERSION = "a"
    BAD_DUMP = "b"
    CRACKED = "cr"
    DOCUMENTATION = "d"
    HACK = "h"
    TRAINED = "t"
    OVERDUMP = "o"
    PIRATE = "p"
    MODIFIED = "m"
    FIXED = "f"


SYSTEMS = ["16K", "48K", "128K", "48K-128K"]


@datasclass(frozen=True)
class TosecFile:
    title: str
    year: str
    publisher: str
    extension: str
    flags: List[FLAG]
    filename: str = ""
    language: str = ""
    country: str = ""
    system: str = ""
    alternative_name: str = ""
    modification: str = ""
    hack: str = ""
    more_info: str = ""
    media: str = ""
    demo: str = ""


class ParserError(Exception):
    pass


class Parser:
    TITLE_PATTERN = r"^(.*?) \("
    YEAR_PATTERN = r"\(([\d\-x]+)\)\("
    PUBLISHER_PATTERN = r"\((.*?)\)"
    EXTENSION_PATTERN = r"\.(.*)"
    FLAGS_PATTERN = r"\[(\w)\]"
    FLAGS_WITH_EXTRA_PATTERN = r"\[(\w+)\s(.*?)\]"
    LANGUAGE_PATTERN = r"\(([a-z]{2})\)"
    COUNTRY_PATTERN = r"\(([A-Z]{2})\)"
    ALTERNATIVE_NAME_PATTERN = r"\[aka (.*)\]"
    MORE_INFO_PATTERN = r"\[(.*)\]"
    MEDIA_PATTERN = r"\((.*)\)[\[\.]"
    DEMO_PATTERN = r"\((demo.*?)\)"

    def parse(self, filename: str) -> TosecFile:
        original_filename = filename
        title, filename = self._extract_field(filename, self.TITLE_PATTERN, 0)
        demo, filename = self._extract_field(filename, self.DEMO_PATTERN, 1)
        year, filename = self._extract_field(filename, self.YEAR_PATTERN, 0)
        publisher, filename = self._extract_field(filename, self.PUBLISHER_PATTERN, 1)
        language, filename = self._extract_field(filename, self.LANGUAGE_PATTERN, 1)
        country, filename = self._extract_field(filename, self.COUNTRY_PATTERN, 1)
        system, filename = self._extract_system(filename)
        media, filename = self._extract_field(filename, self.MEDIA_PATTERN, 0)
        alternative_name, filename = self._extract_field(
            filename, self.ALTERNATIVE_NAME_PATTERN, 1
        )
        flags, filename = self._get_flags(filename)
        flag, extra, filename = self._extract_flag_with_extra(filename)
        if flag:
            flags.append(flag)

        more_info, filename = self._extract_field(filename, self.MORE_INFO_PATTERN, 1)
        extension, filename = self._extract_field(filename, self.EXTENSION_PATTERN, 1)

        if filename.strip():
            raise ParserError(f"Could not parse parts: {filename}")

        return TosecFile(
            filename=original_filename,
            title=title,
            year=year,
            publisher=publisher,
            extension=extension,
            language=language,
            country=country,
            system=system,
            alternative_name=alternative_name,
            flags=flags,
            modification=extra if flag == FLAG.MODIFIED else "",
            hack=extra if flag == FLAG.HACK else "",
            more_info=more_info,
            media=media,
            demo=demo,
        )

    def _get_flags(self, filename: str) -> Tuple[List[FLAG], str]:
        flags = re.search(self.FLAGS_PATTERN, filename)
        if not flags:
            return [], filename
        return (
            [FLAG(flag) for flag in flags.group(1)] if flags else [],
            filename.replace(f"[{flags.group(1)}]", ""),
        )

    def _extract_flag_with_extra(self, filename: str) -> Tuple[FLAG | None, str, str]:
        default = None, "", filename

        flags = re.search(self.FLAGS_WITH_EXTRA_PATTERN, filename)

        if not flags:
            return default

        flag = flags.group(1)
        extra = flags.group(2)

        if flag not in [f.value for f in FLAG]:
            return default

        return (
            FLAG(flag),
            extra,
            filename.replace(f"[{flag} {extra}]", ""),
        )

    def _extract_system(self, filename: str) -> Tuple[str, str]:
        for system in SYSTEMS:
            if f"({system})" in filename:
                return system, filename.replace(f"({system})", "")
        return "", filename

    def _extract_field(
        self, filename: str, pattern: str, extra_count: int
    ) -> Tuple[str, str]:
        logger.debug(f"Extracting {pattern} from {filename}")

        res = re.search(pattern, filename)
        if res:
            field = res.groups()[0]
            filename = filename[: res.start()] + filename[res.end() - 1 + extra_count :]

            logger.debug(f"Extracted {field} result: {filename}")
            return field, filename

        logger.debug(f"Could not find {pattern} in {filename}")
        return "", filename
