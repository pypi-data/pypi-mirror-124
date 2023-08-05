
def build_url(base_url: str, *paths: str) -> str:
    url = base_url

    for path in paths:
        url = url.rstrip("/") + "/" + path.lstrip("/")

    return url


def remove_base(url: str, base: str) -> str:
    return url.replace(base, "")
