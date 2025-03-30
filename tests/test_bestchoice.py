from parser import FLAG

from filters import get_bestchoice_filter
from fixtures import create_tosec_file


def test_return_empty_list():
    bestchoice = get_bestchoice_filter()
    assert bestchoice([]) == []


def test_choose_single_element():
    bestchoice = get_bestchoice_filter()
    files = [create_tosec_file("Werewolves of London")]
    assert bestchoice(files) == files


def test_choose_prefrered_format():
    bestchoice = get_bestchoice_filter(formats=["tap", "z80"])
    files = [
        create_tosec_file("Werewolves of London", extension="z80"),
        create_tosec_file("Werewolves of London", extension="tap"),
    ]
    assert bestchoice(files) == [files[1]]


def test_choose_prefrered_format_with_no_match():
    bestchoice = get_bestchoice_filter(formats=["tap", "z80"])

    files = [
        create_tosec_file("Werewolves of London", extension="tzx"),
        create_tosec_file("Werewolves of London", extension="z80"),
    ]

    assert bestchoice(files) == [files[1]]


def test_choose_one_file_for_every_game_title():
    bestchoice = get_bestchoice_filter(formats=["tap", "z80"])

    files = [
        create_tosec_file("Werewolves of London", extension="z80"),
        create_tosec_file("Another Game", extension="tap"),
        create_tosec_file("Werewolves of London", extension="tap"),
    ]

    assert files[1] in bestchoice(files)
    assert files[2] in bestchoice(files)
    assert files[0] not in bestchoice(files)


def test_choose_one_file_for_every_game_title_and_publisher():
    bestchoice = get_bestchoice_filter(formats=["tap", "z80"])

    files = [
        create_tosec_file("Werewolves of London", extension="tap"),
        create_tosec_file(
            "Werewolves of London", publisher="Whatever", extension="z80"
        ),
        create_tosec_file("Another Game", extension="tap"),
    ]

    assert bestchoice(files) == [files[2], files[0], files[1]]


def test_prefer_games_without_flags():
    bestchoice = get_bestchoice_filter(formats=["tap", "z80"])

    files = [
        create_tosec_file("Werewolves of London", flags=[FLAG.ALTERNATE_VERSION]),
        create_tosec_file("Werewolves of London"),
    ]

    assert bestchoice(files) == [files[1]]


def test_prefered_language():
    bestchoice = get_bestchoice_filter(
        formats=["tap", "z80"], languages=["pl", "en", ""]
    )

    files = [
        create_tosec_file("Werewolves of London", language="es"),
        create_tosec_file("Werewolves of London"),
        create_tosec_file("Werewolves of London", language="pl"),
        create_tosec_file("Werewolves of London", language="en"),
    ]

    assert bestchoice(files) == [files[2]]
