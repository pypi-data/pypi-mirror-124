import pytest

from milena.sip.tools import (
    parse_authentication_info_header,
    parse_parameters_of_header,
    parse_response_header,
    parse_request_header,
    parse_cseq_header,
    parse_uri,
    parse_aor,
)

from ..tools import URIS, AOR_LIST, CSEQ_HEADER_LIST, AUTHENTICATION_INFO_HEADER_LIST


SIP_HEADER_PARAMETERS_LIST = [
    {
        "got": ";tag=76341",
        "expected": {"tag": "76341"},
    },
    {
        "got": ";branch=z9hG4bKfw19b",
        "expected": {"branch": "z9hG4bKfw19b"},
    },
    {
        "got": ";branch=z9hG4bKfw19b;received=100.101.102.103",
        "expected": {"branch": "z9hG4bKfw19b", "received": "100.101.102.103"},
    },
    {
        "got": ";ws",
        "expected": {"ws": None},
    },
    {
        "got": "",
        "expected": {},
    },
]


@pytest.mark.parametrize("case", URIS)
def test_parse_uri_results(case):
    uri = case["string"]
    expected = case["dictionary"]
    alert = "the result of the parse was not what was expected"
    assert parse_uri(uri) == expected, alert


def test_parse_uri_with_invalid_uri():
    with pytest.raises(RuntimeError) as exc:
        parse_uri("sip@alice-192.0.2.4")

    expected = "Invalid URI"
    alert = "the result of the parse was not what was expected"
    assert str(exc.value) == expected, alert


def test_parse_request_header_with_valid_header():
    got = parse_request_header("REGISTER sip:10.10.1.99 SIP/2.0")
    expected = ("REGISTER", 2.0, "sip:10.10.1.99")
    assert got == expected, "The result of the parser was not what was expected"


def test_parse_request_header_with_invalid_header():
    with pytest.raises(RuntimeError) as exc:
        parse_request_header("REGISTER sip:10.10.1.99 WS/2.0")

    expected = "Invalid header on request parsing"
    alert = "The result of the parser was not what was expected"
    assert str(exc.value) == expected, alert


@pytest.mark.parametrize("case", AUTHENTICATION_INFO_HEADER_LIST)
def test_parse_authentication_info_header(case):
    got = parse_authentication_info_header(case["string"])
    expected = case["dictionary"]
    assert got == expected, "The header was not parsed as expected"


def test_parse_authentication_info_header_with_invalid_header():
    with pytest.raises(RuntimeError) as exc:
        parse_authentication_info_header("")

    expected = "Could not parse authentication-info header"
    assert str(exc.value) == expected, "Parser behavior is wrong"


@pytest.mark.parametrize("case", SIP_HEADER_PARAMETERS_LIST)
def test_parse_parameters_of_header(case):
    got = parse_parameters_of_header(case["got"])
    expected = case["expected"]
    assert got == expected, "The parameters was not parsed as expected"


def test_parse_response_header_with_valid_header():
    got = parse_response_header("SIP/2.0 401 Unauthorized")
    expected = (2.0, 401, "Unauthorized")
    assert got == expected, "The result of the parser was not what was expected"


def test_parse_response_header_with_invalid_header():
    with pytest.raises(RuntimeError) as exc:
        parse_response_header("SIP/2 401 Unauthorized")

    expected = "Invalid header on response parsing"
    alert = "The result of the parser was not what was expected"
    assert str(exc.value) == expected, alert


@pytest.mark.parametrize("case", CSEQ_HEADER_LIST)
def test_parse_cseq_header(case):
    got = parse_cseq_header(case["string"])
    expected = case["dictionary"]
    assert got == expected, "The header was not parsed as expected"


def test_parse_cseq_header_with_invalid_header():
    with pytest.raises(RuntimeError) as exc:
        parse_cseq_header("")

    expected = "Could not parse cseq header"
    assert str(exc.value) == expected, "Parser behavior is wrong"


@pytest.mark.parametrize("case", AOR_LIST)
def test_parse_aor(case):
    got = parse_aor(case["string"])
    expected = case["dictionary"]
    assert got == expected, "The parameters was not parsed as expected"


def test_parse_aor_with_invalid_aor():
    with pytest.raises(RuntimeError) as exc:
        parse_aor("")

    expected = "Invalid AOR: ''"
    assert str(exc.value) == expected, "Parser behavior is wrong"
