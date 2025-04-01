from parser import FLAG

import pytest

from grouper import get_group_by
from tests.fixtures import create_tosec_file


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


def test_dir_limit_not_divisible():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter(
        [
            create_tosec_file(title="Werewolves of London"),
            create_tosec_file(title="Airewolves of London"),
            create_tosec_file(title="world Series Baseball"),
            create_tosec_file(title="world Series Baseball 2"),
            create_tosec_file(title="world Series Baseball 3"),
            create_tosec_file(title="Xanadu"),
        ],
        3,
    ) == {
        "A": [
            create_tosec_file(title="Airewolves of London"),
        ],
        "W#-WM": [
            create_tosec_file(title="Werewolves of London"),
        ],
        "WN-WZ": [
            create_tosec_file(title="world Series Baseball"),
            create_tosec_file(title="world Series Baseball 2"),
            create_tosec_file(title="world Series Baseball 3"),
        ],
        "X": [
            create_tosec_file(title="Xanadu"),
        ],
    }


def test_dir_limit_exceeds_alphabet():
    group_by_first_letter = get_group_by()

    files = [create_tosec_file(title=f"A{chr(65+i)} Title") for i in range(30)]

    result = group_by_first_letter(
        files,
        1,
    )
    assert len(list(result.keys())) == 26


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
        "W#-WM": [
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


def test_limit_with_special_characters():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter(
        [
            create_tosec_file(title="!A Othello", language="en"),
            create_tosec_file(title="1A Othello", language="en"),
            create_tosec_file(title="A Othello", language="en"),
            create_tosec_file(title="AR Othello", language="en"),
            create_tosec_file(title="C1 Othello", language="en"),
            create_tosec_file(title="CO Othello", language="en"),
        ],
        1,
    ) == {
        "#": [
            create_tosec_file(title="!A Othello", language="en"),
            create_tosec_file(title="1A Othello", language="en"),
        ],
        "A#-AM": [
            create_tosec_file(title="A Othello", language="en"),
        ],
        "AN-AZ": [
            create_tosec_file(title="AR Othello", language="en"),
        ],
        "C#-CM": [
            create_tosec_file(title="C1 Othello", language="en"),
        ],
        "CN-CZ": [
            create_tosec_file(title="CO Othello", language="en"),
        ],
    }


def test_limit_similar_counts():
    group_by_first_letter = get_group_by()

    assert group_by_first_letter(
        [
            create_tosec_file(title="AAA"),
            create_tosec_file(title="AAB"),
            create_tosec_file(title="AAC"),
            create_tosec_file(title="ABA"),
            create_tosec_file(title="AOA"),
            create_tosec_file(title="ASA"),
        ],
        3,
    ) == {
        "A#-AA": [
            create_tosec_file(title="AAA"),
            create_tosec_file(title="AAB"),
            create_tosec_file(title="AAC"),
        ],
        "AB-AZ": [
            create_tosec_file(title="ABA"),
            create_tosec_file(title="AOA"),
            create_tosec_file(title="ASA"),
        ],
    }
