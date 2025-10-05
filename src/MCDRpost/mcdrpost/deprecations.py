from mcdreforged import PluginServerInterface
from typing_extensions import NamedTuple

from mcdrpost.constants import PLUGIN_ID
from mcdrpost.utils.version import SemanticVersion


class Deprecation(NamedTuple):
    feature: str
    version_deprecated: str
    version_removal: str
    instead_info: str | None = None


class Deprecations:
    __TEMPLATE = "{} is deprecated in v{}, and will be removed in v{}."
    __INSTEAD_INFO_TEMPLATE = "Please use {} instead"

    def __init__(self, *features: tuple | Deprecation):
        self.features = (
            feature if isinstance(feature, Deprecation) else Deprecation(*feature)
            for feature in features
        )

    def log(self, server: PluginServerInterface):
        plg_vers = SemanticVersion(str(server.get_plugin_metadata(PLUGIN_ID).version))

        has_warned: bool = False

        for feature in self.features:
            # noinspection PyTypeChecker
            if feature.version_deprecated <= plg_vers < feature.version_removal:
                server.logger.warning(self.__TEMPLATE.format(*feature))
                if feature.instead_info:
                    server.logger.warning(self.__INSTEAD_INFO_TEMPLATE.format(feature.instead_info))

                has_warned = True

        if has_warned:
            server.logger.warning("Please discontinue these features as soon as possible.")


DEPRECATIONS: Deprecations = Deprecations(
    ("configuration `command_permission`", "3.4.0", "3.6", "`permissions`"),
    ("configuration `command_prefixes`", "3.4.0", "3.6", "`prefix`"),
    ("configuration `allow_alias`", "3.4.0", "3.6", "`prefix`"),
)
