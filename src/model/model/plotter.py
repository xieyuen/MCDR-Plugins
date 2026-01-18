import numpy as np
from matplotlib import pyplot as plt
from mcdreforged import PluginServerInterface

from model.configuration import Configuration


class Plotter:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        self.logger = server.logger
        self.config = server.load_config_simple(
            target_class=Configuration,
            file_format="yaml",
        )

    def formular_1(self, t):
        A = self.config.plot_args.A
        B = self.config.plot_args.B
        C = B / (4 * A)

        return (
            (B / 2) * t + C - C * np.exp(-2 * A * t),
            (B / 2) * t - C + C * np.exp(-2 * A * t),
        )

    def formular_1_asymptote(self, t):
        A = self.config.plot_args.A
        B = self.config.plot_args.B
        C = B / (4 * A)

        return (
            (B / 2) * t + C,
            (B / 2) * t - C
        )

    def formular_2(self, t):
        A = self.config.plot_args.A
        B = self.config.plot_args.B
        C2 = B / (4 * A)
        C1 = -C2
        C3 = C2 + self.config.plot_args.v_0

        return (
            C3 - C2 * np.exp(-2 * A * t),
            C1 + C2 * np.exp(-2 * A * t)
        )

    def formular_2_asymptote(self, _t):
        return self.config.plot_args.v_0 / 2

    def show(self):
        plt.xlabel("t")
        plt.ylabel("v")
        plt.show()

    def log_args(self):
        self.logger.info("正在使用以下参数作图：")
        self.logger.info("A = {0}, B = {1}".format(self.config.plot_args.A, self.config.plot_args.B))
        self.logger.info(f"是否绘制渐近线: {self.config.asymptote}")

    def plot_1(self):
        self.show()

    def plot_2(self):
        self.show()
