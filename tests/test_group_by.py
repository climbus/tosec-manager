from parser import FLAG, TosecFile

from grouper import get_group_by


def test_group_by_first_letter_empty_list():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter([]) == {}


def test_group_by_first_letter():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter(
        [
            TosecFile(
                filename="Werewolves of London (1989)(Mastertronic).tap",
                title="Werewolves of London",
                year="1989",
                publisher="Mastertronic",
                extension="tap",
                flags=[],
            ),
            TosecFile(
                filename="World Series Baseball (1985)(Imagine)[a].z80",
                title="World Series Baseball",
                year="1985",
                publisher="Imagine",
                extension="z80",
                flags=[FLAG.ALTERNATE_VERSION],
            ),
            TosecFile(
                filename="Othello (2008)(YRS)(en).tap",
                title="Othello",
                year="2008",
                publisher="YRS",
                extension="tap",
                language="en",
                flags=[],
            ),
            TosecFile(
                filename="'Rthello (2008)(YRS)(NL).tap",
                title="Rthello",
                year="2008",
                publisher="YRS",
                extension="tap",
                country="NL",
                flags=[],
            ),
        ]
    ) == {
        "W": [
            TosecFile(
                filename="Werewolves of London (1989)(Mastertronic).tap",
                title="Werewolves of London",
                year="1989",
                publisher="Mastertronic",
                extension="tap",
                flags=[],
            ),
            TosecFile(
                filename="World Series Baseball (1985)(Imagine)[a].z80",
                title="World Series Baseball",
                year="1985",
                publisher="Imagine",
                extension="z80",
                flags=[FLAG.ALTERNATE_VERSION],
            ),
        ],
        "O": [
            TosecFile(
                filename="Othello (2008)(YRS)(en).tap",
                title="Othello",
                year="2008",
                publisher="YRS",
                extension="tap",
                language="en",
                flags=[],
            ),
        ],
        "R": [
            TosecFile(
                filename="'Rthello (2008)(YRS)(NL).tap",
                title="Rthello",
                year="2008",
                publisher="YRS",
                extension="tap",
                country="NL",
                flags=[],
            ),
        ],
    }


def test_group_by_first_letter_as_number_and_special_char():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter(
        [
            TosecFile(
                filename="1K Othello (2008)(YRS)(en).tap",
                title="1K Othello",
                year="2008",
                publisher="YRS",
                extension="tap",
                language="en",
                flags=[],
            ),
            TosecFile(
                filename="!K Othello (2008)(YRS)(en).tap",
                title="!K Othello",
                year="2008",
                publisher="YRS",
                extension="tap",
                language="en",
                flags=[],
            ),
        ]
    ) == {
        "#": [
            TosecFile(
                filename="1K Othello (2008)(YRS)(en).tap",
                title="1K Othello",
                year="2008",
                publisher="YRS",
                extension="tap",
                language="en",
                flags=[],
            ),
            TosecFile(
                filename="!K Othello (2008)(YRS)(en).tap",
                title="!K Othello",
                year="2008",
                publisher="YRS",
                extension="tap",
                language="en",
                flags=[],
            ),
        ],
    }


def test_dir_uppercase():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter(
        [
            TosecFile(
                filename="Werewolves of London (1989)(Mastertronic).tap",
                title="Werewolves of London",
                year="1989",
                publisher="Mastertronic",
                extension="tap",
                flags=[],
            ),
            TosecFile(
                filename="world Series Baseball (1985)(Imagine)[a].z80",
                title="world Series Baseball",
                year="1985",
                publisher="Imagine",
                extension="z80",
                flags=[],
            ),
        ]
    ) == {
        "W": [
            TosecFile(
                filename="Werewolves of London (1989)(Mastertronic).tap",
                title="Werewolves of London",
                year="1989",
                publisher="Mastertronic",
                extension="tap",
                flags=[],
            ),
            TosecFile(
                filename="world Series Baseball (1985)(Imagine)[a].z80",
                title="world Series Baseball",
                year="1985",
                publisher="Imagine",
                extension="z80",
                flags=[],
            ),
        ],
    }


def test_dir_limit():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter(
        [
            TosecFile(
                filename="Werewolves of London (1989)(Mastertronic).tap",
                title="Werewolves of London",
                year="1989",
                publisher="Mastertronic",
                extension="tap",
                flags=[],
            ),
            TosecFile(
                filename="world Series Baseball (1985)(Imagine)[a].z80",
                title="world Series Baseball",
                year="1985",
                publisher="Imagine",
                extension="z80",
                flags=[],
            ),
        ],
        1,
    ) == {
        "WA-WM": [
            TosecFile(
                filename="Werewolves of London (1989)(Mastertronic).tap",
                title="Werewolves of London",
                year="1989",
                publisher="Mastertronic",
                extension="tap",
                flags=[],
            ),
        ],
        "WM-WZ": [
            TosecFile(
                filename="world Series Baseball (1985)(Imagine)[a].z80",
                title="world Series Baseball",
                year="1985",
                publisher="Imagine",
                extension="z80",
                flags=[],
            ),
        ],
    }
