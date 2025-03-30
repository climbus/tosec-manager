from parser import FLAG

import pytest

from fixtures import create_tosec_file
from grouper import get_group_by


def test_group_by_first_letter_empty_list():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter([]) == {}


def test_group_by_first_letter():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter(
        [
            create_tosec_file(title="Werewolves of London"),
            create_tosec_file(
                title="World Series Baseball", flags=[FLAG.ALTERNATE_VERSION]
            ),
            create_tosec_file(title="Othello", language="en"),
            create_tosec_file(title="Rthello", country="NL"),
        ]
    ) == {
        "W": [
            create_tosec_file(title="Werewolves of London"),
            create_tosec_file(
                title="World Series Baseball", flags=[FLAG.ALTERNATE_VERSION]
            ),
        ],
        "O": [
            create_tosec_file(title="Othello", language="en"),
        ],
        "R": [
            create_tosec_file(title="Rthello", country="NL"),
        ],
    }


def test_group_by_first_letter_as_number_and_special_char():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter(
        [
            create_tosec_file(title="1K Othello", language="en"),
            create_tosec_file(title="!K Othello", language="en"),
        ]
    ) == {
        "#": [
            create_tosec_file(title="1K Othello", language="en"),
            create_tosec_file(title="!K Othello", language="en"),
        ],
    }


def test_dir_uppercase():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter(
        [
            create_tosec_file(title="Werewolves of London"),
            create_tosec_file(title="world Series Baseball"),
        ]
    ) == {
        "W": [
            create_tosec_file(title="Werewolves of London"),
            create_tosec_file(title="world Series Baseball"),
        ],
    }


def test_dir_limit():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter(
        [
            create_tosec_file(title="Werewolves of London"),
            create_tosec_file(title="Airewolves of London"),
            create_tosec_file(title="world Series Baseball"),
        ],
        1,
    ) == {
        "A": [
            create_tosec_file(title="Airewolves of London"),
        ],
        "WA-WM": [
            create_tosec_file(title="Werewolves of London"),
        ],
        "WN-WZ": [
            create_tosec_file(title="world Series Baseball"),
        ],
    }


@pytest.mark.skip
def test_limit_with_numbers():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter(
        [
            create_tosec_file(title="1K Othello", language="en"),
            create_tosec_file(title="!K Othello", language="en"),
        ],
        1,
    ) == {
        "##-#M": [create_tosec_file(title="1K Othello", language="en")],
        "#N-#Z": [
            create_tosec_file(title="!K Othello", language="en"),
        ],
    }
