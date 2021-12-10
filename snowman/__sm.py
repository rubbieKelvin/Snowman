from typing import Tuple
from typing import Final

APPNAME = "Snowman"
VERSION = (0, 0, 1)
__email__: Final = "dev.rubbie@gmail.com"
__authour__: Final = "Rubbie Kelvin Voltman"

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


__version__: Final = version_tuple_to_str(VERSION)
