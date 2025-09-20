import re
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


@total_ordering
class MinecraftVersion(SemanticVersion):
    # Minecraft版本映射表，将快照版本映射到对应的主版本
    SNAPSHOT_MAPPING = {
        # 1.19 snapshots
        (22, 11): "1.19.3",
        (22, 12): "1.19.3",
        (22, 13): "1.19.3",
        (22, 14): "1.19.3",
        (22, 15): "1.19.3",
        (22, 16): "1.19.3",
        (22, 17): "1.19.3",
        (22, 18): "1.19.3",
        (22, 19): "1.19.3",
        (22, 20): "1.19.3",
        (22, 21): "1.19.3",
        (22, 22): "1.19.3",
        (22, 23): "1.19.3",
        (22, 24): "1.19.4",
        (22, 25): "1.19.4",
        (22, 26): "1.19.4",
        (22, 27): "1.19.4",
        (22, 42): "1.19.3",
        (22, 43): "1.19.3",
        (22, 44): "1.19.3",
        (22, 45): "1.19.4",
        (22, 46): "1.19.4",
        (22, 47): "1.19.4",
        (22, 49): "1.19.4",
        (22, 50): "1.19.4",
        (22, 51): "1.19.4",

        # 1.20 snapshots
        (23, 1): "1.20",
        (23, 2): "1.20",
        (23, 3): "1.20",
        (23, 4): "1.20",
        (23, 5): "1.20",
        (23, 6): "1.20",
        (23, 7): "1.20",
        (23, 9): "1.20.1",
        (23, 10): "1.20.1",
        (23, 12): "1.20.1",
        (23, 13): "1.20.1",
        (23, 14): "1.20.1",
        (23, 16): "1.20.1",
        (23, 18): "1.20.1",
        (23, 19): "1.20.1",
        (23, 20): "1.20.1",
        (23, 21): "1.20.1",
        (23, 22): "1.20.1",
        (23, 23): "1.20.1",
        (23, 24): "1.20.1",
        (23, 25): "1.20.1",
        (23, 26): "1.20.1",
        (23, 27): "1.20.1",
        (23, 28): "1.20.1",
        (23, 30): "1.20.2",
        (23, 31): "1.20.2",
        (23, 32): "1.20.2",
        (23, 33): "1.20.2",
        (23, 34): "1.20.2",
        (23, 35): "1.20.2",
        (23, 36): "1.20.2",
        (23, 40): "1.20.3",
        (23, 41): "1.20.3",
        (23, 42): "1.20.3",
        (23, 43): "1.20.3",
        (23, 44): "1.20.3",
        (23, 45): "1.20.3",
        (23, 46): "1.20.3",
        (23, 48): "1.20.3",
        (23, 49): "1.20.3",
        (23, 50): "1.20.3",
        (23, 51): "1.20.3",
        (23, 52): "1.20.3",

        # 1.20.5 snapshots
        (24, 1): "1.20.4",
        (24, 2): "1.20.4",
        (24, 3): "1.20.4",
        (24, 4): "1.20.4",
        (24, 5): "1.20.5",
        (24, 6): "1.20.5",
        (24, 7): "1.20.5",
        (24, 9): "1.20.5",
        (24, 10): "1.20.5",
        (24, 11): "1.20.5",
        (24, 12): "1.20.5",
        (24, 13): "1.20.5",
        (24, 14): "1.20.5",
        (24, 15): "1.20.5",
        (24, 16): "1.20.5",
        (24, 17): "1.20.5",
        (24, 18): "1.20.5",
        (24, 20): "1.20.5",
        (24, 21): "1.20.5",
    }

    def __init__(self, version_string: str) -> None:
        # 检查是否为Minecraft快照格式 (如 14w22a)
        snapshot_pattern = re.compile(r'^(\d{2})w(\d{2})([a-z])$')
        match = snapshot_pattern.match(version_string)

        if match:
            # 对于快照版本，我们创建一个特殊的版本对象
            self.snapshot_version = version_string
            self.is_snapshot = True
            # 将快照版本转换为可比较的格式
            year, week, letter = match.groups()
            # 创建一个特殊的版本元组用于比较
            # 格式: (year, week, letter_index, 0, 0, 0)
            letter_index = ord(letter) - ord('a')
            self.version_tuple = (int(year), int(week), letter_index, 0, 0, 0)

            # 映射快照版本到对应的正式版本
            year_week = (int(year), int(week))
            if year_week in self.SNAPSHOT_MAPPING:
                self.mapped_version = SemanticVersion(self.SNAPSHOT_MAPPING[year_week])
            else:
                # 如果没有映射，则默认为一个较低的版本
                self.mapped_version = SemanticVersion("0.0.0")
        else:
            self.is_snapshot = False
            super().__init__(version_string)

    def __eq__(self, other: 'MinecraftVersion | str') -> bool:
        if isinstance(other, str):
            other = MinecraftVersion(other)

        if self.is_snapshot and other.is_snapshot:
            return self.version_tuple == other.version_tuple
        elif not self.is_snapshot and not other.is_snapshot:
            return super().__eq__(other)
        elif self.is_snapshot and not other.is_snapshot:
            # 快照版本与正式版本比较 - 快照版本应该比对应的正式版本低
            return self.mapped_version.version == other.version
        elif not self.is_snapshot and other.is_snapshot:
            # 正式版本与快照版本比较
            return self.version == other.mapped_version.version
        else:
            return False

    def __lt__(self, other: 'MinecraftVersion | str') -> bool:
        if isinstance(other, str):
            other = MinecraftVersion(other)

        if self.is_snapshot and other.is_snapshot:
            return self.version_tuple < other.version_tuple
        elif not self.is_snapshot and not other.is_snapshot:
            return super().__lt__(other)
        elif self.is_snapshot and not other.is_snapshot:
            # 快照版本应该比对应的正式版本低
            return self.mapped_version.version < other.version
        elif not self.is_snapshot and other.is_snapshot:
            # 正式版本与快照版本比较
            return self.version < other.mapped_version.version
        else:
            return False

    def __str__(self) -> str:
        if self.is_snapshot:
            return self.snapshot_version
        return super().__str__()

    def __repr__(self) -> str:
        if self.is_snapshot:
            return f'MinecraftVersion({self.snapshot_version!r})'
        return f'MinecraftVersion({str(self)!r})'
