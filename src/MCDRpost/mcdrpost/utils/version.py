from functools import total_ordering
from typing import NamedTuple, TypeAlias, TypeVar

from packaging import version

SemanticVersionType = TypeVar('SemanticVersionType', bound='SemanticVersion')
SimpleVersionTupleType = TypeVar('SimpleVersionTupleType', bound='SimpleVersionTuple')
VersionTupleType: TypeAlias = (
        tuple[int, int]
        | tuple[int, int, int]
        | tuple[int, int, int, str]
        | tuple[int, int, int, str, str]
)
SupportOperateType: TypeAlias = str | SemanticVersionType | VersionTupleType | SemanticVersionType


class SimpleVersionTuple(NamedTuple):
    major: int
    minor: int
    patch: int = 0
    pre_release: str = ''
    build_info: str = ''

    @property
    def __version_string(self):
        s = f'{self.major}.{self.minor}.{self.patch}'
        if self.pre_release:
            s += f'-{self.pre_release}'
        if self.build_info:
            s += f'+{self.build_info}'

        return s

    def to_semantic_version(self) -> SemanticVersionType:
        return SemanticVersion(self.__version_string)


@total_ordering
class SemanticVersion:
    """语义化版本号

    Attributes:
        version (packaging.version.Version): 直接被 packaging 解析得到的 Version 对象
        major (int): 主版本号
        minor (int): 次版本号
        patch (int): 补丁版本号
        pre_release (tuple[str, int] | None): 预发布版本号
        build_metadata (tuple[str, int] | None): 构建元数据
    """

    def __init__(self, version_string: str) -> None:
        self.version = version.parse(version_string)
        self.major = self.version.major
        self.minor = self.version.minor
        self.patch = self.version.micro
        self.pre_release = self.version.pre
        self.build_metadata = self.version.local

    @property
    def is_pre_release(self) -> bool:
        """是否是预发布版本"""
        return self.pre_release is not None

    @staticmethod
    def __param_normalize(param: SupportOperateType) -> SemanticVersionType:
        if isinstance(param, str):
            return SemanticVersion(param)
        elif isinstance(param, tuple):
            return SimpleVersionTuple(*param).to_semantic_version()
        elif isinstance(param, SemanticVersion):
            return param
        else:
            return NotImplemented

    def __eq__(self, other) -> bool:
        other = self.__param_normalize(other)
        if other is NotImplemented:
            return False

        return self.version == other.version

    def __lt__(self, other) -> bool:
        other = self.__param_normalize(other)
        if other is NotImplemented:
            return NotImplemented

        return self.version < other.version

    def __str__(self) -> str:
        return str(self.version)

    def __repr__(self) -> str:
        return f'SemanticVersion({str(self.version)!r})'
