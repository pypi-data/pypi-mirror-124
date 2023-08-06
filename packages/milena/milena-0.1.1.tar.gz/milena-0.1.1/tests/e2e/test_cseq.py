import pytest

from milena.sip import CSeq

from ..tools import CSEQ_HEADER_LIST


@pytest.mark.parametrize("case", CSEQ_HEADER_LIST)
def test_CSeq_string_interface(case):
    string = case["string"]
    dictionary = case["dictionary"]
    alert = "the result of the string interface was not what was expected"

    instance = CSeq.setup("dict", dictionary)
    assert instance.string() == string, alert


@pytest.mark.parametrize("case", CSEQ_HEADER_LIST)
def test_CSeq_print(case):
    string = case["string"]
    dictionary = case["dictionary"]
    alert = "the result of the string interface was not what was expected"

    instance = CSeq.setup("dict", dictionary)
    assert str(instance) == f"CSeq: {string}", alert


@pytest.mark.parametrize("case", CSEQ_HEADER_LIST)
def test_CSeq_dict_interface(case):
    string = case["string"]
    dictionary = case["dictionary"]
    alert = "the result of the dictionary interface was not what was expected"

    instance = CSeq.setup("string", string)
    assert instance.dict() == dictionary, alert


def test_CSeq_without_content():
    with pytest.raises(ValueError) as exc:
        _ = CSeq()

    expected = "You need to enter a valid dictionary or a string"
    assert str(exc.value) == expected, "CSeq init need raise an error"


def test_uri_with_invalid_uri():
    with pytest.raises(ValueError) as exc:
        _ = CSeq(string="Cseq: Register 123")

    expected = "Invalid sip CSeq header format"
    assert str(exc.value) == expected, "CSeq init need raise an error"
