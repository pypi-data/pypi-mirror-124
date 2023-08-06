import pytest

from milena.sip.tools import (
    stringify_cseq_header,
    stringify_auth_header,
    stringify_parameters,
    stringify_headers,
    stringify_uri,
    stringify_aor,
)

from ..tools import URIS, AOR_LIST, CSEQ_HEADER_LIST, AUTHENTICATION_INFO_HEADER_LIST

PARAMETERS = [
    {"dictionary": {}, "string": ""},
    {"dictionary": {"rport": None}, "string": ";rport"},
    {"dictionary": {"method": "REGISTER"}, "string": ";method=REGISTER"},
    {
        "dictionary": {"method": "REGISTER", "rport": None},
        "string": ";method=REGISTER;rport",
    },
]

HEADERS = [
    {"dictionary": {}, "string": ""},
    {"dictionary": {"to": "alice%40atlanta.com"}, "string": "?to=alice%40atlanta.com"},
    {
        "dictionary": {"subject": "project%20x", "priority": "urgent"},
        "string": "?subject=project%20x&priority=urgent",
    },
]


@pytest.mark.parametrize("case", PARAMETERS)
def test_stringify_parameters_results(case):
    string = case["string"]
    dictionary = case["dictionary"]
    alert = "the result of the parse was not what was expected"
    assert stringify_parameters(";", dictionary) == string, alert


@pytest.mark.parametrize("case", HEADERS)
def test_stringify_headers_results(case):
    string = case["string"]
    dictionary = case["dictionary"]
    alert = "the result of the parse was not what was expected"
    assert stringify_headers(dictionary) == string, alert


@pytest.mark.parametrize("case", URIS)
def test_stringify_uri_results(case):
    uri = case["string"]
    dictionary = case["dictionary"]
    alert = "the result of the stringify was not what was expected"
    assert stringify_uri(dictionary) == uri, alert


@pytest.mark.parametrize("case", AOR_LIST)
def test_stringify_aor_results(case):
    uri = case["string"]
    dictionary = case["dictionary"]
    alert = "the result of the stringify was not what was expected"
    assert stringify_aor(dictionary) == uri, alert


@pytest.mark.parametrize("case", CSEQ_HEADER_LIST)
def test_parse_cseq_header(case):
    got = stringify_cseq_header(case["dictionary"])
    expected = case["string"]
    assert got == expected, "the result of the stringify was not what was expected"


@pytest.mark.parametrize("case", AUTHENTICATION_INFO_HEADER_LIST)
def test_parse_authentication_info_header(case):
    got = stringify_auth_header(case["dictionary"])
    expected = case["string"]
    assert got == expected, "the result of the stringify was not what was expected"
