from typing import Tuple

APPNAME = "Snowman"
VERSION = (1, 0, 0)

def version_tuple_to_str(version: Tuple[int, int, int]) -> str:
    return '.'.join([str(i) for i in version])

def version_tuple_from_str(version: str) -> Tuple[int, ...]:
    return tuple([int(i) for i in version.split('.')])
