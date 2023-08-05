import base64


def add_padding(s: str) -> str:
    return s + "=" * ((4 - len(s) % 4) % 4)


def b64_trim_padding(s: str) -> str:
    return s.rstrip("=")


def urlsafe_b64decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(add_padding(s))


def urlsafe_b64encode_to_string(b: bytes, trim_padding=False) -> str:
    result = base64.urlsafe_b64encode(b).decode("utf-8")

    if trim_padding:
        result = b64_trim_padding(result)

    return result


def b64encode_without_padding(s: str) -> str:
    return b64_trim_padding(base64.b64encode(s.encode()).decode("utf-8"))
