from typing import Dict, Optional

from .eval import is_valid_uri
from .etc import DictUri


def stringify_parameters(delimiter: str, parameters: Dict[str, Optional[str]]) -> str:
    result = ""

    for key, value in parameters.items():
        result += f"{delimiter}{key}={value}" if value else f"{delimiter}{key}"

    return result


def stringify_headers(headers: Dict[str, Optional[str]]) -> str:
    array = [key + "=" + str(value) for key, value in headers.items()]
    result = ("?" + "&".join(array)) if array else ""
    return result


def stringify_uri(dictionary: DictUri) -> str:
    parameters = stringify_parameters(";", dictionary.get("parameters", {}))
    headers = stringify_headers(dictionary.get("headers", {}))
    schema = dictionary.get("schema", "sip")
    password = dictionary.get("password")
    user = dictionary.get("user")
    host = dictionary.get("host")
    port = dictionary.get("port")

    result = f"{schema}:"

    if user:
        result += f"{user}:{password}@" if password else f"{user}@"

    result += f"{host}"

    if port:
        result += f":{port}"

    result += parameters
    result += headers

    return result


def stringify_aor(aor: Dict[str, Optional[str]]):
    name = aor.get("name") if aor.get("name") else ""

    if is_valid_uri(aor.get("uri", "")):
        uri = f"<{aor.get('uri')}>"
    else:
        uri = aor.get("uri")

    parameters = stringify_parameters(";", aor.get("parameters", {}))

    return f"{name} {uri}{parameters}".strip()


def stringify_cseq_header(cseq: Dict[str, str]) -> str:
    method = cseq["method"].upper()
    return f'{cseq["seq"]} {method}'


def stringify_auth_header(header: Dict[str, Optional[str]]) -> str:
    scheme = header.pop("scheme", None)
    parameters = stringify_parameters(",", header)[1:]

    if scheme:
        result = f"{scheme} {parameters}"
    else:
        result = parameters

    return result
