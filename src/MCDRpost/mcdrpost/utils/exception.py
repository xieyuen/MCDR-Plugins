class DataError(ValueError):
    pass


class InvalidOrder(DataError):
    pass


class InvalidItem(DataError):
    pass


class InvalidConfig(DataError):
    pass


class InvalidPermission(InvalidConfig):
    pass


class InvalidPrefix(InvalidConfig):
    pass
