from abc import ABC, abstractmethod


class TotalOrdering[ComparableType](ABC):
    @abstractmethod
    def __eq__(self, other) -> bool:  # self == other
        raise NotImplementedError

    @abstractmethod
    def __lt__(self, other: ComparableType) -> bool:  # self < other
        raise NotImplementedError

    def __le__(self, other: ComparableType) -> bool:  # self <= other
        return self < other or self == other

    def __gt__(self, other: ComparableType) -> bool:  # self > other
        return not (self <= other)

    def __ge__(self, other: ComparableType) -> bool:  # self >= other
        return not (self < other)
