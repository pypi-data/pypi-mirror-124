from typing import Tuple, Dict, Union, Optional
from urllib.parse import unquote

from .regex import URI, SIP, HEADERS
from .etc import DictUri


def parse_uri(uri: str) -> DictUri:
    match = URI["field"].match(uri)

    if not match:
        raise RuntimeError("Invalid URI")

    schema = match.group(1)
    user = match.group(2)
    password = match.group(3)
    host = match.group(4)

    port = None
    if match.group(5):
        port = int(match.group(5))

    parameters = dict()
    if match.group(6):
        iterable = URI["parameters"].finditer(match.group(6))
        for parameter in iterable:
            if parameter.group(3):
                parameters[parameter.group(1)] = parameter.group(3)
            else:
                parameters[parameter.group(1)] = None

    headers = dict()
    if match.group(7):
        iterable = URI["headers"].finditer(match.group(7))
        for header in iterable:
            headers[header.group(1)] = header.group(2)

    return {
        "schema": schema,
        "user": user,
        "password": password,
        "host": host,
        "port": port,
        "parameters": parameters,
        "headers": headers,
    }


def parse_response_header(header: str) -> Tuple[float, int, str]:
    match = SIP["response"].match(header)

    if not match:
        raise RuntimeError("Invalid header on response parsing")

    version = float(match.group(2))
    status = int(match.group(3))
    reason = match.group(4)

    return version, status, reason


def parse_request_header(header: str) -> Tuple[float, int, str]:
    match = SIP["request"].match(header)

    if not match:
        raise RuntimeError("Invalid header on request parsing")

    method = unquote(match.group(1))
    version = float(match.group(3))
    uri = match.group(2)

    return method, version, uri


def parse_authentication_info_header(header: str) -> Dict[str, str]:
    result = dict()

    while True:
        match = HEADERS["authentication-info"].match(header)

        if not match:
            raise RuntimeError("Could not parse authentication-info header")

        key = match.group(1)
        value = match.group(2)
        result[key] = value

        header = header[match.end() :]

        if not header or header[0] != ",":
            break

        header = header[1:].lstrip()

    return result


def parse_cseq_header(header: str) -> Dict[str, Union[str, int]]:
    match = HEADERS["cseq"].match(header)

    if not match:
        raise RuntimeError("Could not parse cseq header")

    seq = int(match.group(1))
    method = unquote(match.group(2))

    return {"seq": seq, "method": method}


def parse_parameters_of_header(header: str) -> Dict[str, str]:
    result = dict()

    while True:
        match = HEADERS["parameters"].match(header)

        if not match:
            break

        key = match.group(1).lower()
        value = match.group(2)
        result[key] = value

        header = header[match.end() :]

    return result


def parse_aor(aor: str) -> Dict[str, Union[str, Optional[str]]]:
    match = SIP["aor"].match(aor)

    if not match:
        raise RuntimeError(f"Invalid AOR: '{aor}'")

    name = match.group(1)

    if match.group(2):
        uri = match.group(2)

    elif match.group(3):
        uri = match.group(3)

    parameters = parse_parameters_of_header(aor[match.end() :])
    result = {"name": name, "uri": uri, "parameters": parameters}

    return result
