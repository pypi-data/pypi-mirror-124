import pytest

from milena.sip import AOR

from ..tools import AOR_LIST

INVALID_AOR_LIST = [
    {"dictionary": {"user": "user"}},
]


@pytest.mark.parametrize("case", AOR_LIST)
def test_AOR_string_interface(case):
    string = case["string"]
    dictionary = case["dictionary"]
    alert = "the result of the string interface was not what was expected"

    instance = AOR.setup("dict", dictionary)
    assert instance.string() == string, alert


@pytest.mark.parametrize("case", AOR_LIST)
def test_AOR_print(case):
    string = case["string"]
    dictionary = case["dictionary"]
    alert = "the result of the string interface was not what was expected"

    instance = AOR.setup("dict", dictionary)
    assert str(instance) == string, alert


@pytest.mark.parametrize("case", AOR_LIST)
def test_AOR_dict_interface(case):
    string = case["string"]
    dictionary = case["dictionary"]
    alert = "the result of the dictionary interface was not what was expected"

    instance = AOR.setup("string", string)
    assert instance.dict() == dictionary, alert


def test_AOR_without_content():
    with pytest.raises(ValueError) as exc:
        _ = AOR()

    expected = "You need to enter a valid dictionary or a string AOR"
    assert str(exc.value) == expected, "AOR init need raise an error"


@pytest.mark.parametrize("case", INVALID_AOR_LIST)
def test_uri_with_invalid_uri(case):
    with pytest.raises(ValueError) as exc:
        _ = AOR(**case)

    expected = "Invalid sip AOR format"
    assert str(exc.value) == expected, "AOR init need raise an error"


def test_uri_with_invalid_source_on_setup():
    with pytest.raises(RuntimeError) as exc:
        _ = AOR.setup(source="", content="sip:user@domain.com&123=1123")

    expected = "Invalid source format"
    assert str(exc.value) == expected, "URI init need raise an error"
