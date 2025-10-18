import warnings

from mcdreforged import PluginServerInterface
from typing_extensions import NamedTuple

from mcdrpost.constants import PLUGIN_ID
from mcdrpost.utils.version import SemanticVersion

_TEMPLATE = "{} is deprecated in v{}, and will be removed in v{}."
_INSTEAD_INFO_TEMPLATE = "Please use {} instead"


class _Deprecation(NamedTuple):
    feature: str
    version_deprecated: str
    version_removal: str
    instead_info: str | None = None

    def log(self, server: PluginServerInterface):
        server.logger.warning(_TEMPLATE.format(self.feature, self.version_deprecated, self.version_removal))
        if self.instead_info:
            server.logger.warning(_INSTEAD_INFO_TEMPLATE.format(self.instead_info))

    @property
    def __msg(self) -> str:
        msg = _TEMPLATE.format(self.feature, self.version_deprecated, self.version_removal)
        if self.instead_info:
            msg += " " + _INSTEAD_INFO_TEMPLATE.format(self.instead_info)
        return msg

    def warn(self):
        warnings.warn(self.__msg, FutureWarning)


class _Deprecations:
    def __init__(self, *features: tuple[str, str, str, str] | _Deprecation):
        self.features = (_Deprecation(*feature) for feature in features)

    def log(self, server: PluginServerInterface):
        plugin_version: SemanticVersion = SemanticVersion(str(server.get_plugin_metadata(PLUGIN_ID).version))
        has_warned: bool = False

        for feature in self.features:
            if feature.version_deprecated <= plugin_version < feature.version_removal:
                feature.log(server)
                has_warned = True

        if has_warned:
            server.logger.warning("Please discontinue these features as soon as possible.")


# TODO: Deprecations
DEPRECATIONS: _Deprecations = _Deprecations(
    ("configuration `command_permission`", "3.4.0", "3.6", "`permissions`"),
    ("configuration `command_prefixes`", "3.4.0", "3.6", "`prefix`"),
    ("configuration `allow_alias`", "3.4.0", "3.6", "`prefix`"),
)

__all__ = ['DEPRECATIONS']
