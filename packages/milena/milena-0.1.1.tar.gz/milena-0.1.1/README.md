# What is Milena?

[![Gitpod badge](https://img.shields.io/badge/Gitpod-ready%20to%20code-908a85?logo=gitpod)](https://gitpod.io/#https://github.com/Otoru/Milena)
[![Tests badge](https://github.com/Otoru/Milena/actions/workflows/tests.yml/badge.svg)](https://github.com/Otoru/Milena/actions/workflows/tests.yml)
[![License badge](https://img.shields.io/github/license/otoru/Milena.svg)](https://github.com/Otoru/milena/blob/Milena/LICENSE.md)

milena is a SIP stack made for us to create testing tools for anyone working with VoIP.

## API References

Most of our classes follow a very similar API, providing `.string()` and `.dict()` methods to access information either raw or with a native python interface.

### SIP URI

The SIP URI is a Uniform Resource Identifier (URI) scheme for the Session Initiation Protocol (SIP) multimedia communications protocol. A SIP address is a URI that addresses a specific telephone extension on a voice over IP system. Such a number could be a private branch exchange or an E.164 telephone number dialled through a specific gateway. The scheme was defined in RFC 3261.

By [wikipedia](https://en.wikipedia.org/wiki/SIP_URI_scheme).

#### Example

```python
from milena.sip import URI

string = "sip:alice@atlanta.com"
dictionary = {
    "schema": "sip",
    "user": "alice",
    "password": None,
    "host": "atlanta.com",
    "port": None,
    "parameters": {},
    "headers": {},
}

alice = URI.setup(source="string", content=string)
assert alice.string() == string
assert alice.dict() == dictionary

alice = URI.setup(source="dict", content=dictionary)
assert alice.string() == string
assert alice.dict() == dictionary
```

#### Exceptions

- In case an incorrect parameter will be passed to the API we will have an exception of type `ValueError`.
- In case of a failure during the parse or stringify process we will have an exception of type `RuntimeError`.

### Address of Record

A address of record (AOR) is very similar to a SIP URI, except that it can carry some more information, such as the display name.

#### Example

```python
from milena.sip import AOR

string = "Alice <sip:alice@atlanta.example.com>;tag=9fxced76sl"
dictionary = {
    "name": "Alice",
    "uri": "sip:alice@atlanta.example.com",
    "parameters": {
        "tag": "9fxced76sl"
    },
}

alice = URI.setup(source="string", content=string)
assert alice.string() == string
assert alice.dict() == dictionary

alice = URI.setup(source="dict", content=dictionary)
assert alice.string() == string
assert alice.dict() == dictionary
```

#### Exceptions

- In case an incorrect parameter will be passed to the API we will have an exception of type `ValueError`.
- In case of a failure during the parse or stringify process we will have an exception of type `RuntimeError`.

### Sip Headers

Here is a list of implemented sip headers with a brief code demo.

#### CSeq

```python
from milena.sip import CSeq

string = "4711 INVITE",
dictionary = {"seq": 4711, "method": "INVITE"}

header = CSeq.setup(source="string", content=string)
assert header.string() == string
assert header.dict() == dictionary

header = CSeq.setup(source="dict", content=dictionary)
assert header.string() == string
assert header.dict() == dictionary

print(header)
# CSeq: 4711 INVITE
```

#### Authentication Info

```python
from milena.sip import AuthenticationInfo

string = 'nextnonce="47364c23432d2e131a5fb210812c",qop="auth,auth-int"',
dictionary = {
    "nextnonce": '"47364c23432d2e131a5fb210812c"',
    "qop": '"auth,auth-int"',
}

header = AuthenticationInfo.setup(source="string", content=string)
assert header.string() == string
assert header.dict() == dictionary

header = AuthenticationInfo.setup(source="dict", content=dictionary)
assert header.string() == string
assert header.dict() == dictionary

print(header)
# CSeq: 4711 INVITE
```

#### Exceptions

- In case an incorrect parameter will be passed to the SIP header API we will have an exception of type `ValueError`.
- In case of a failure during the parse or stringify process we will have an exception of type `RuntimeError`.

### Comments

- By design choice, the properties of each API are read-only. If you want to change a certain value, work with a copy of the API dictionary you want to change and then create a new instance.
- APIs have a `setup` method that must be used to inform if we are using it from a `string` or a `dict`.
- By design choice, the `string` method will return the value of the formatted SIP header, but converting the object to a literal string (`str(API)`) will return the header in key=value format, ready to go. used on your User Agent.

## How to contribute?

If you are thinking of contributing in any way to the project, you will be very welcome. Whether it's improving existing documentation, suggesting new features or running existing bugs, it's only by working together that the project will grow.

Do not forget to see our [Contributing Guide][2] and our [Code of Conduct][3] to always be aligned with the ideas of the project.

[2]: https://github.com/Otoru/Milena/blob/master/CONTRIBUTING.md
[3]: https://github.com/Otoru/Milena/blob/master/CODE_OF_CONDUCT.md

## Contributors

Will be welcome ❤️

## Author

| [<img src="https://avatars0.githubusercontent.com/u/26543872?v=3&s=115"><br><sub>@Otoru</sub>](https://github.com/Otoru) |
| :----------------------------------------------------------------------------------------------------------------------: |
