from parser import FLAG, TosecFile

from filters import get_bestchoice_filter


def test_return_empty_list():
    bestchoice = get_bestchoice_filter()
    assert bestchoice([]) == []


def test_choose_single_element():
    bestchoice = get_bestchoice_filter()
    files = [
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic).tap",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="tap",
            flags=[],
        )
    ]
    assert bestchoice(files) == files


def test_choose_prefrered_format():
    bestchoice = get_bestchoice_filter(formats=["tap", "z80"])
    files = [
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic).tap",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="z80",
            flags=[],
        ),
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic).z80",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="tap",
            flags=[],
        ),
    ]
    assert bestchoice(files) == [files[1]]


def test_choose_prefrered_format_with_no_match():
    bestchoice = get_bestchoice_filter(formats=["tap", "z80"])

    files = [
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic).tzx",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="tzx",
            flags=[],
        ),
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic).z80",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="z80",
            flags=[],
        ),
    ]

    assert bestchoice(files) == [files[1]]


def test_choose_one_file_for_every_game_title():
    bestchoice = get_bestchoice_filter(formats=["tap", "z80"])

    files = [
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic).tap",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="tap",
            flags=[],
        ),
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic).z80",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="z80",
            flags=[],
        ),
        TosecFile(
            filename="Another Game (1989)(Mastertronic).tap",
            title="Another Game",
            year="1989",
            publisher="Mastertronic",
            extension="tap",
            flags=[],
        ),
    ]

    assert bestchoice(files) == [files[0], files[2]]


def test_choose_one_file_for_every_game_title_and_publisher():
    bestchoice = get_bestchoice_filter(formats=["tap", "z80"])

    files = [
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic).tap",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="tap",
            flags=[],
        ),
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic).z80",
            title="Werewolves of London",
            year="1989",
            publisher="Whatever",
            extension="z80",
            flags=[],
        ),
        TosecFile(
            filename="Another Game (1989)(Mastertronic).tap",
            title="Another Game",
            year="1989",
            publisher="Mastertronic",
            extension="tap",
            flags=[],
        ),
    ]

    assert bestchoice(files) == [files[0], files[1], files[2]]


def test_prefer_games_without_flags():
    bestchoice = get_bestchoice_filter(formats=["tap", "z80"])

    files = [
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic).tap",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="tap",
            flags=[FLAG.ALTERNATE_VERSION],
        ),
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic)[a].tap",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="tap",
            flags=[],
        ),
    ]

    assert bestchoice(files) == [files[1]]


def test_prefered_language():
    bestchoice = get_bestchoice_filter(
        formats=["tap", "z80"], languages=["pl", "en", ""]
    )

    files = [
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic)(pl).tap",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="tap",
            language="es",
            flags=[],
        ),
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic).tap",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="tap",
            flags=[],
        ),
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic)(en).tap",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="tap",
            language="pl",
            flags=[],
        ),
        TosecFile(
            filename="Werewolves of London (1989)(Mastertronic)(en).tap",
            title="Werewolves of London",
            year="1989",
            publisher="Mastertronic",
            extension="tap",
            language="en",
            flags=[],
        ),
    ]

    assert bestchoice(files) == [files[2]]
