import re
from types import NotImplementedType
from typing import Any, NamedTuple, TypeAlias, TypeVar, overload

from mcdrpost.utils import TotalOrdering

ValidVersionTupleType: TypeAlias = (  # TODO: 替换成 3.12 的语法
        tuple[int, int]  # major and minor, its patch version will be set to 0
        # major, minor, patch
        | tuple[int, int, int]
        # major, minor, patch, pre_release
        | tuple[int, int, int, str]
        # major, minor, patch, pre_release, build_metadata
        # pre_release cannot be None, but can be an empty str for a non-pre-release version
        | tuple[int, int, int, str, str]
)
SemanticVersionType = TypeVar("SemanticVersionType", bound="SemanticVersion")


class SimpleVersionTuple(NamedTuple):
    major: int
    minor: int
    patch: int = 0
    pre_release: str = ''
    build_metadata: str = ''

    @property
    def __version_string(self):
        s = f'{self.major}.{self.minor}.{self.patch}'
        if self.pre_release:
            s += f'-{self.pre_release}'
        if self.build_metadata:
            s += f'+{self.build_metadata}'

        return s

    def to_semantic_version(self) -> "SemanticVersion":
        return SemanticVersion(self.__version_string)


class SemanticVersion(
    TotalOrdering[SemanticVersionType | SimpleVersionTuple | ValidVersionTupleType | str]
):
    """语义化版本号

    Attributes:
        major (int): 主版本号
        minor (int): 次版本号
        patch (int): 补丁版本号
        pre_release (tuple[str, int] | None): 预发布版本号
        build_metadata (tuple[str, int] | None): 构建元数据
    """
    PATTERN = re.compile(
        r'^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$'
    )

    major: int
    minor: int
    patch: int
    pre_release: str | None = None
    build_metadata: str | None = None

    def __init__(self, version_str: str) -> None:
        self._original_string = version_str

        match = re.match(self.PATTERN, version_str)
        if not match:
            raise ValueError(f'Invalid version string: {version_str}')

        major, minor, patch, self.pre_release, self.build_metadata = match.groups()

        if any(i is None for i in [major, minor, patch]):
            raise ValueError(f'Invalid semantic version string: {version_str}')

        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)

    @property
    def is_pre_release(self) -> bool:
        """是否是预发布版本"""
        return self.pre_release is not None

    @overload
    @staticmethod
    def __param_normalize(param: SemanticVersionType) -> SemanticVersionType:
        ...

    @overload
    @staticmethod
    def __param_normalize(param: str) -> SemanticVersionType:
        ...

    @overload
    @staticmethod
    def __param_normalize(param: SimpleVersionTuple) -> SemanticVersionType:
        ...

    @overload
    @staticmethod
    def __param_normalize(param: ValidVersionTupleType) -> SemanticVersionType:
        ...

    @overload
    @staticmethod
    def __param_normalize(param: Any) -> NotImplementedType:
        ...

    @staticmethod
    def __param_normalize(param):
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

        return (
                (self.major, self.minor, self.patch, self.pre_release)
                == (other.major, other.minor, other.patch, other.pre_release)
        )

    @staticmethod
    def __compare_pre_release(pre1: str, pre2: str) -> bool:
        """比较预发布版本号"""
        parts1 = pre1.split('.')
        parts2 = pre2.split('.')

        for p1, p2 in zip(parts1, parts2):
            # 尝试转换为数字比较，否则按字符串比较
            try:
                num1, num2 = int(p1), int(p2)
                if num1 != num2:
                    return num1 < num2
            except ValueError:
                if p1 != p2:
                    return p1 < p2

        # 如果共同部分都相同，长度短的更小
        return len(parts1) < len(parts2)

    def __lt__(self, other) -> bool:
        n_other = self.__param_normalize(other)
        if n_other is NotImplemented:
            return NotImplemented

        if (self.major, self.minor, self.patch) < (n_other.major, n_other.minor, n_other.patch):
            return True
        elif (self.major, self.minor, self.patch) > (n_other.major, n_other.minor, n_other.patch):
            return False
        elif self.pre_release is None:
            return False
        elif n_other.pre_release is None:
            return True
        return self.__compare_pre_release(self.pre_release, n_other.pre_release)

    def __str__(self) -> str:
        return self._original_string

    def __repr__(self) -> str:
        return f'SemanticVersion(major={self.major}, minor={self.minor}, patch={self.patch}, pre_release={self.pre_release}, build_metadata={self.build_metadata})'
