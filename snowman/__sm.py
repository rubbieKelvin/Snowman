from typing import Tuple

APPNAME = "Snowman"
VERSION = (1, 0, 0)

def version_tuple_to_str(version: Tuple[int, int, int]) -> str:
    return '.'.join([str(i) for i in version])

def version_tuple_from_str(version: str) -> Tuple[int|None, int|None, int|None]:
    version = version.strip()
    
    if len(version) == 0:
        return VERSION

    res = [int(i) for i in version.split('.')]

    if len(res) > 3:
        raise TypeError(f'Invalid version type "{version}"')

    return tuple([ *res, *([None]*(3-len(res))) ])
