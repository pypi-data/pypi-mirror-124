import pytest

from milena.sip import URI

from ..tools import URIS

INVALID_URI_LIST = [
    {"string": "sip:user@domain.com&123=1123"},
    {"dictionary": {"user": "user"}},
]


@pytest.mark.parametrize("case", URIS)
def test_URI_string_interface(case):
    string = case["string"]
    dictionary = case["dictionary"]
    alert = "the result of the string interface was not what was expected"

    instance = URI.setup("dict", dictionary)
    assert instance.string() == string, alert


@pytest.mark.parametrize("case", URIS)
def test_URI_print(case):
    string = case["string"]
    dictionary = case["dictionary"]
    alert = "the result of the string interface was not what was expected"

    instance = URI.setup("dict", dictionary)
    assert str(instance) == string, alert


@pytest.mark.parametrize("case", URIS)
def test_URI_dict_interface(case):
    string = case["string"]
    dictionary = case["dictionary"]
    alert = "the result of the dictionary interface was not what was expected"

    instance = URI.setup("string", string)
    assert instance.dict() == dictionary, alert


def test_uri_without_content():
    with pytest.raises(ValueError) as exc:
        _ = URI()

    expected = "You need to enter a valid dictionary or a string sip URI"
    assert str(exc.value) == expected, "URI init need raise an error"


@pytest.mark.parametrize("case", INVALID_URI_LIST)
def test_uri_with_invalid_uri(case):
    with pytest.raises(ValueError) as exc:
        _ = URI(**case)

    expected = "Invalid sip URI format"
    assert str(exc.value) == expected, "URI init need raise an error"


def test_uri_with_invalid_source_on_setup():
    with pytest.raises(RuntimeError) as exc:
        _ = URI.setup(source="", content="sip:user@domain.com&123=1123")

    expected = "Invalid source format"
    assert str(exc.value) == expected, "URI init need raise an error"
