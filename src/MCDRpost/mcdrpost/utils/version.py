import functools
import re
from typing import Any, NamedTuple, Protocol


def compare_pre(pre: str, other: str) -> bool:
    pre_parts = pre.split('.') if pre else []
    other_parts = other.split('.') if other else []
    for p, o in zip(pre_parts, other_parts):
        if p.isdigit() and o.isdigit():
            if int(p) > int(o):
                return True
            elif int(p) < int(o):
                return False
        else:
            if p > o:
                return True
            elif p < o:
                return False
    return len(pre_parts) > len(other_parts)


class ComparableType(Protocol):
    major: int
    minor: int
    patch: int
    prerelease: str
    build: str

    @property
    def is_prerelease(self) -> bool:
        raise NotImplementedError


class VersionTuple(NamedTuple):
    major: int
    minor: int
    patch: int = 0
    prerelease: str = ""
    build: str = ""

    @property
    def is_prerelease(self) -> bool:
        return self.prerelease != ""


@functools.total_ordering
class MCVersion(ComparableType):
    """Minecraft 版本解析类

    此类实现了 Minecraft 版本的解析, 无论是新命名系统还是旧系统, 都可以正确解析.
    并且此类实现了版本之间的比较. 不仅限于 MCVersion 实例, 还可以与合法的版本字符串和
    合法的 tuple 实例比较
    """

    major: int = 0
    """主版本号"""
    minor: int = 0
    """次版本号"""
    patch: int = 0
    """补丁版本号"""
    prerelease: str = ""
    """预发布版本号"""
    build: str = ""
    """构建元数据"""

    VERSION_PATTERN = re.compile(
        r"^(\d+)\.(\d+)(?:\.(\d+))?(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$",
    )

    def __init__(self, version_str: str):
        if not isinstance(version_str, str):
            raise TypeError("Invalid version string")

        if not version_str:
            raise ValueError("Version string cannot be empty")

        match = self.VERSION_PATTERN.fullmatch(version_str)
        if not match:
            raise ValueError("Invalid version string")
        self.major = int(match.group(1))
        self.minor = int(match.group(2))
        self.patch = int(match.group(3)) if match.group(3) else 0
        self.prerelease = match.group(4) or ""
        self.build = match.group(5) or ""

    @property
    def is_prerelease(self) -> bool:
        return self.prerelease != ""

    def __repr__(self):
        return f"MCVersion(major={self.major}, minor={self.minor}, patch={self.patch}, prerelease='{self.prerelease}', build='{self.build}')"

    def __str__(self):
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version

    @staticmethod
    def __normalize(param: Any) -> ComparableType:
        if isinstance(param, MCVersion):
            return param
        elif isinstance(param, str):
            return MCVersion(param)
        elif isinstance(param, tuple):
            return VersionTuple(*param)  # type: ignore
        else:
            raise TypeError(f"Cannot compare MCVersion with {type(param)}")

    def __eq__(self, other) -> bool:
        try:
            target = self.__normalize(other)
        except (ValueError, TypeError):
            return False

        return all(
            [
                self.major == target.major,
                self.minor == target.minor,
                self.patch == target.patch,
                self.prerelease == target.prerelease,
            ],
        )

    def __gt__(self, other) -> bool:
        try:
            target = self.__normalize(other)
        except (ValueError, TypeError):
            return NotImplemented

        if self.major > target.major:
            return True
        elif self.major < target.major:
            return False
        elif self.minor > target.minor:
            return True
        elif self.minor < target.minor:
            return False
        elif self.patch > target.patch:
            return True
        elif self.patch < target.patch:
            return False

        if not self.is_prerelease:
            return target.is_prerelease
        if not target.is_prerelease:
            return False

        return compare_pre(self.prerelease, target.prerelease)
