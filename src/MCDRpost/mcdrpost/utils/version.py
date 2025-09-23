from functools import total_ordering

from packaging import version


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

    def __eq__(self, other: 'SemanticVersion | str') -> bool:
        if isinstance(other, str):
            other = SemanticVersion(other)
        return self.version == other.version

    def __lt__(self, other: 'SemanticVersion | str') -> bool:
        if isinstance(other, str):
            other = SemanticVersion(other)
        return self.version < other.version

    def __str__(self) -> str:
        return str(self.version)

    def __repr__(self) -> str:
        return f'SemanticVersion({str(self.version)!r})'
