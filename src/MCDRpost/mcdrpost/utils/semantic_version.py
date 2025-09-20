from functools import total_ordering

from packaging import version


@total_ordering
class SemanticVersion:
    def __init__(self, version_string: str) -> None:
        self.version = version.parse(version_string)
        self.major = self.version.major
        self.minor = self.version.minor

        # 定义patch版本号，优先使用micro属性，否则从release元组中获取
        if hasattr(self.version, 'micro'):
            self.patch = self.version.micro
        else:
            # 从release元组中获取patch版本，如果不存在则默认为0
            if len(self.version.release) > 2:
                self.patch = self.version.release[2]
            else:
                self.patch = 0

        self.pre_release = self.version.pre
        self.build_metadata = self.version.local

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
