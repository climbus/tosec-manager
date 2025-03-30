from parser import FLAG, Parser, ParserError, TosecFile

import pytest


def test_parse_single_simple_element():
    parser = Parser()

    filename = "Werewolves of London (1989)(Mastertronic).tap"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="Werewolves of London",
        year="1989",
        publisher="Mastertronic",
        extension="tap",
        flags=[],
    )


def test_parse_single_element_with_flag():
    parser = Parser()

    filename = "World Series Baseball (1985)(Imagine)[a].z80"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="World Series Baseball",
        year="1985",
        publisher="Imagine",
        extension="z80",
        flags=[FLAG.ALTERNATE_VERSION],
    )


def test_parse_single_element_with_language():
    parser = Parser()

    filename = "1K Othello (2008)(YRS)(en).tap"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="1K Othello",
        year="2008",
        publisher="YRS",
        extension="tap",
        language="en",
        flags=[],
    )


def test_parse_single_element_with_country():
    parser = Parser()

    filename = "1K Othello (2008)(YRS)(NL).tap"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="1K Othello",
        year="2008",
        publisher="YRS",
        extension="tap",
        country="NL",
        flags=[],
    )


def test_parse_with_system():
    parser = Parser()

    filename = "Andy Capp (1988)(Mirrorsoft)(128K).z80"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="Andy Capp",
        year="1988",
        publisher="Mirrorsoft",
        extension="z80",
        system="128K",
        flags=[],
    )


def test_parse_alternative_name():
    parser = Parser()

    filename = "Almost Bosconian (2014)(Amore)[aka Forget Bosconian].tap"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="Almost Bosconian",
        year="2014",
        publisher="Amore",
        extension="tap",
        alternative_name="Forget Bosconian",
        flags=[],
    )


def test_parse_two_systems():
    parser = Parser()

    filename = "Big Javi's Adventure, The (2017-03-29)(Metsuke)(48K-128K).tap"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="Big Javi's Adventure, The",
        year="2017-03-29",
        publisher="Metsuke",
        extension="tap",
        system="48K-128K",
        flags=[],
    )


def test_parse_modified_flag():
    parser = Parser()

    filename = "Bolalela 2 (2008)(BeykerSoft)[m tzxtools].tap"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="Bolalela 2",
        year="2008",
        publisher="BeykerSoft",
        extension="tap",
        flags=[FLAG.MODIFIED],
        modification="tzxtools",
    )


def test_parse_hack_flag():
    parser = Parser()

    filename = "Bolalela 2 (2008)(BeykerSoft)[h tzxtools].tap"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="Bolalela 2",
        year="2008",
        publisher="BeykerSoft",
        extension="tap",
        flags=[FLAG.HACK],
        hack="tzxtools",
    )


def test_parse_publisher_with_spaces():
    parser = Parser()

    filename = "Bolalela 2 (2008)(Beyker Soft).tap"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="Bolalela 2",
        year="2008",
        publisher="Beyker Soft",
        extension="tap",
        flags=[],
    )


def test_parse_smth():
    parser = Parser()

    filename = "07 Zglos Sie (19xx)(Kuba Rozpruwacz)(PL)[m tzxtools].tap"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="07 Zglos Sie",
        year="19xx",
        publisher="Kuba Rozpruwacz",
        extension="tap",
        country="PL",
        flags=[FLAG.MODIFIED],
        modification="tzxtools",
    )


def test_parse_more_info():
    parser = Parser()

    filename = "10 PRINT Hello - GO TO 10 Randomly Lineinput Version (2009)(Guesser)(16K)[CSSCGC].tap"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="10 PRINT Hello - GO TO 10 Randomly Lineinput Version",
        year="2009",
        publisher="Guesser",
        extension="tap",
        system="16K",
        flags=[],
        more_info="CSSCGC",
    )


def test_parse_media():
    parser = Parser()

    filename = "19 Part 1 - Boot Camp - Megatape 1 (demo) (1988)(Cascade Games)(48K-128K)(Side B)[m tzxtools][Sinclair User Covertape].pok"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="19 Part 1 - Boot Camp - Megatape 1",
        year="1988",
        publisher="Cascade Games",
        extension="pok",
        system="48K-128K",
        flags=[FLAG.MODIFIED],
        modification="tzxtools",
        more_info="Sinclair User Covertape",
        media="Side B",
        demo="demo",
    )


def test_parse_with_parentesis_in_hack():
    parser = Parser()

    filename = "Blade Warrior (1988)(Code Masters)(48K-128K)[h Ely (Msi)].pok"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="Blade Warrior",
        year="1988",
        publisher="Code Masters",
        extension="pok",
        system="48K-128K",
        flags=[FLAG.HACK],
        hack="Ely (Msi)",
    )


def test_parse_missing_year():
    parser = Parser()

    filename = "Game Without Year ()(Publisher).tap"
    with pytest.raises(ParserError):
        parser.parse(filename)


def test_parse_missing_publisher():
    parser = Parser()

    filename = "Game Without Publisher (1989)().tap"
    with pytest.raises(ParserError):
        parser.parse(filename)


def test_parse_invalid_format():
    parser = Parser()

    filename = "Invalid Format Game 1989 Publisher.tap"
    with pytest.raises(ParserError):
        parser.parse(filename)


def test_parse_unexpected_characters():
    parser = Parser()

    filename = "Unexpected!Characters (1989)(Publisher).tap"
    assert parser.parse(filename) == TosecFile(
        filename=filename,
        title="Unexpected!Characters",
        year="1989",
        publisher="Publisher",
        extension="tap",
        flags=[],
    )
