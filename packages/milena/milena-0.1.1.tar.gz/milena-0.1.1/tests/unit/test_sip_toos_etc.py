import pytest

from milena.sip.tools import (
    split_sip_message,
    split_sip_header,
)

from ..tools import REGISTER, prepare_message


SIP_HEADER = [
    {"string": "CSeq: 1 REGISTER", "array": ("cseq", "1 REGISTER")},
    {
        "string": "Via: SIP/2.0/UDP 10.10.1.13:5060;branch=z9hG4bK78946131-99e1-de11-8845-080027608325;rport",
        "array": (
            "via",
            "SIP/2.0/UDP 10.10.1.13:5060;branch=z9hG4bK78946131-99e1-de11-8845-080027608325;rport",
        ),
    },
    {
        "string": "User-Agent: MySipClient/4.0.0",
        "array": ("user-agent", "MySipClient/4.0.0"),
    },
    {
        "string": "From: <sip:13@10.10.1.99>;tag=d60e6131-99e1-de11-8845-080027608325",
        "array": (
            "from",
            "<sip:13@10.10.1.99>;tag=d60e6131-99e1-de11-8845-080027608325",
        ),
    },
    {"string": "Call-ID: e4ec6031-99e1", "array": ("call-id", "e4ec6031-99e1")},
    {"string": "To: <sip:13@10.10.1.99>", "array": ("to", "<sip:13@10.10.1.99>")},
    {
        "string": "Contact: <sip:13@10.10.1.13>;q=1",
        "array": ("contact", "<sip:13@10.10.1.13>;q=1"),
    },
    {
        "string": "Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,SUBSCRIBE,NOTIFY,REFER,MESSAGE,INFO,PING",
        "array": (
            "allow",
            "INVITE,ACK,OPTIONS,BYE,CANCEL,SUBSCRIBE,NOTIFY,REFER,MESSAGE,INFO,PING",
        ),
    },
    {"string": "Expires: 3600", "array": ("expires", "3600")},
    {"string": "Content-Length: 0", "array": ("content-length", "0")},
    {"string": "Max-Forwards: 70", "array": ("max-forwards", "70")},
]


def test_split_sip_message_with_valid_sip_message():
    message = prepare_message(REGISTER)
    got = split_sip_message(message)
    sip = [
        "REGISTER sip:10.10.1.99 SIP/2.0",
        "CSeq: 1 REGISTER",
        "Via: SIP/2.0/UDP 10.10.1.13:5060;branch=z9hG4bK78946131-99e1-de11-8845-080027608325;rport",
        "User-Agent: MySipClient/4.0.0",
        "From: <sip:13@10.10.1.99>;tag=d60e6131-99e1-de11-8845-080027608325",
        "Call-ID: e4ec6031-99e1",
        "To: <sip:13@10.10.1.99>",
        "Contact: <sip:13@10.10.1.13>;q=1",
        "Allow: INVITE,ACK,OPTIONS,BYE,CANCEL,SUBSCRIBE,NOTIFY,REFER,MESSAGE,INFO,PING",
        "Expires: 3600",
        "Content-Length: 0",
        "Max-Forwards: 70",
    ]
    sdp = ""
    expected = (sip, sdp)
    assert got == expected, "Message not parsed as expected"


def test_split_sip_message_with_invalid_sip_message():
    with pytest.raises(RuntimeError) as exc:
        split_sip_message(REGISTER)

    expected = "Invalid SIP message format, couldn't find header/body division"
    assert str(exc.value) == expected, "Message not parsed as expected"


@pytest.mark.parametrize("case", SIP_HEADER)
def test_split_sip_header_with_valid_uri(case):
    array = case["array"]
    string = case["string"]
    got = split_sip_header(string)
    assert got == array, "Header not parsed as expected"


def test_split_sip_header_with_invalid_uri():
    with pytest.raises(RuntimeError) as exc:
        split_sip_header("CSeq 1 REGISTER")

    expected = "Invalid SIP header. Parsing line: CSeq 1 REGISTER"
    assert str(exc.value) == expected, "Parser behavior is wrong"
