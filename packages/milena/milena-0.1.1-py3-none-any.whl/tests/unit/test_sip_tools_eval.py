import pytest

from milena.sip.tools import is_valid_uri, is_response, is_request

from ..tools import REGISTER, UNAUTHORIZED, prepare_message, URIS


INVALID_URIS = ["sip:;alert=test", "sip:user@domain.com&123=1123"]


def test_identifies_a_request_correctly():
    message = prepare_message(REGISTER)
    message_is_request = is_request(message.splitlines())
    assert message_is_request, "This message is a request!"


def test_identifies_a_response_correctly():
    message = prepare_message(UNAUTHORIZED)
    message_is_response = is_response(message.splitlines())
    assert message_is_response, "This message is a response!"


def test_responses_are_not_identified_as_requests():
    message = prepare_message(UNAUTHORIZED)
    message_is_request = is_request(message.splitlines())
    assert not message_is_request, "This message is a response!"


def test_request_are_not_identified_as_responses():
    message = prepare_message(REGISTER)
    message_is_request = is_response(message.splitlines())
    assert not message_is_request, "This message is a request!"


@pytest.mark.parametrize("case", URIS)
def test_uri_is_valid_with_valid_uri(case):
    uri = case["string"]
    assert is_valid_uri(uri), "This URI should be valid"


@pytest.mark.parametrize("uri", INVALID_URIS)
def test_uri_is_valid_with_invalid_uri(uri):
    assert not is_valid_uri(uri), "This URI should be not valid"
