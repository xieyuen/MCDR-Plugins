from typing import Literal

from mcdreforged import PluginServerInterface

from mcdrpost.data_structure import OrderData
from mcdrpost.utils.translation import TranslationKeys


class DataManager:
    """数据管理类"""

    DATA_FILE = "orders.json"
    DATA_TYPE: Literal["json"] = "json"

    @property
    def data(self) -> OrderData:
        return self._data

    def __init__(self, server: PluginServerInterface):
        self.server = server
        self._data = self._load()

    def _load(self) -> OrderData:
        """加载数据"""
        data = self.server.load_config_simple(
            self.DATA_FILE,
            target_class=OrderData,
            in_data_folder=True,
            file_format=self.DATA_TYPE,
            echo_in_console=False,
        )
        self.server.logger.info(TranslationKeys.data_loaded.rtr())
        return data

    def reload(self):
        self._data = self._load()

    def save(self):
        self.server.save_config_simple(
            self.data,
            self.DATA_FILE,
            in_data_folder=True,
            file_format=self.DATA_TYPE,
        )
        self.server.logger.info(TranslationKeys.data_saved.rtr())
