# pylint: disable=invalid-name
from typing import NamedTuple

__all__ = ('__version__', 'version_info')


class Version(NamedTuple):
    major: int
    minor: int
    micro: int
    tag: str = None

    @classmethod
    def from_str(cls, s: str) -> 'Version':
        major, minor, rest = s.split('.')
        rest_parts = rest.split('-')
        if len(rest_parts) == 1:
            # Just micro
            micro = rest[0]
            tag = None
        else:
            micro, tag = rest_parts
        return cls(int(major), int(minor), int(micro), tag)

    def __str__(self) -> str:
        """The full version as X.Y.Z-tag"""
        s = f'{self.major}.{self.minor}.{self.micro}'
        if self.tag is not None:
            s += f'-{self.tag}'
        return s

    def short_version(self) -> str:
        """The short X.Y version"""
        return f'{self.major}.{self.minor}'


__version__ = '0.0.2'
version_info = Version.from_str(__version__)
