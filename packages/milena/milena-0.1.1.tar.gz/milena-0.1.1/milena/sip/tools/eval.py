from typing import List

from .regex import SIP, URI, HEADERS


def is_request(headers: List[str]) -> bool:
    if SIP["request"].match(headers.pop(0)):
        return True

    return False


def is_response(headers: List[str]) -> bool:
    if SIP["response"].match(headers.pop(0)):
        return True

    return False


def is_valid_uri(uri: str) -> bool:
    if URI["field"].match(uri):
        return True

    return False


def is_valid_cseq_header(header: str) -> bool:
    if HEADERS["cseq"].match(header):
        return True

    return False


def is_valid_auth_info_header(header: str) -> bool:
    if HEADERS["authentication-info"].match(header):
        return True

    return False
