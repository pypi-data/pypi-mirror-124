import re

URI = {
    "field": re.compile(
        r"^(sips?):(?:([^\s>:@]+)(?::([^\s@>]+))?@)?([\w\-\.]+)(?::(\d+))?((?:;[^\s=\?>;]+(?:=[^\s?\;]+)?)*)(?:\?(([^\s&=>]+=[^\s&=>]+)(&[^\s&=>]+=[^\s&=>]+)*))?$"
    ),
    "parameters": re.compile(r"([^;=]+)(=([^;=]+))?"),
    "headers": re.compile(r"([^&=]+)=([^&=]+)"),
}

SIP = {
    "response": re.compile(r"^(\w.*)\/(\d+\.\d+)\s+(\d+)\s*(.*)\s*$"),
    "request": re.compile(r"^([\w\-.!%*_+`'~]+)\s([^\s]+)\sSIP\s*\/\s*(\d+\.\d+)$"),
    "message": re.compile(r"^\s*([\S\s]*?)\r\n\r\n([\S\s]*)$"),
    "headers": re.compile(r"^([\S]*?)\s*:\s*([\s\S]*)$"),
    "aor": re.compile(
        r'((?:[\w\-.!%*_+`\'~]+)(?:\s+[\w\-.!%*_+`\'~]+)*|"[^"\\]*(?:\\.[^"\\]*)*")?\s*\<\s*([^>]*)\s*\>|((?:[^\s@"<]@)?[^\s;]+)'
    ),
}

HEADERS = {
    "authentication-info": re.compile(
        r'([^\s,"=]*)\s*=\s*([^\s,"]+|"[^"\\]*(?:\\.[^"\\]*)*")\s*'
    ),
    "cseq": re.compile(r"(\d+)\s*([\S]+)"),
    "parameters": re.compile(
        r'\s*;\s*([\w\-.!%*_+`\'~]+)(?:\s*=\s*([\w\-.!%*_+`\'~]+|"[^"\\]*(\\.[^"\\]*)*"))?'
    ),
}

SPLIT_LINES = re.compile(r"\r\n(?![ \t])")
