from typing import Optional, Dict, Union, Tuple
from urllib.parse import unquote

from .regex import SIP, SPLIT_LINES

DictUri = Dict[str, Optional[Union[str, Dict[str, Optional[str]]]]]

COMPACT_HEADERS = {
    "i": "call-id",
    "m": "contact",
    "e": "contact-encoding",
    "l": "content-length",
    "c": "content-type",
    "f": "from",
    "s": "subject",
    "k": "supported",
    "t": "to",
    "v": "via",
}

MULTIINSTANCE_HEADERS = (
    "contact",
    "route",
    "record-route",
    "path",
    "via",
    "www-authenticate",
    "authorization",
    "proxy-authenticate",
    "proxy-authorization",
)


def split_sip_message(message: str) -> Tuple[str, str]:
    match = SIP["message"].match(message)

    if not match:
        alert = "Invalid SIP message format, couldn't find header/body division"
        raise RuntimeError(alert)

    else:
        sip = SPLIT_LINES.split(match.group(1))
        sdp = match.group(2)

        return sip, sdp


def split_sip_header(header: str) -> Tuple[str, str]:
    match = SIP["headers"].match(header)

    if not match:
        raise RuntimeError(f"Invalid SIP header. Parsing line: {header}")

    else:
        key = unquote(match.group(1)).lower()
        value = match.group(2)
        return key, value
