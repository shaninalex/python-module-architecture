from slugify import slugify as _slugify


def slugify(title: str) -> str:
    return _slugify(title)