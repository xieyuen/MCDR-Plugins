from mcdreforged import Serializable


class FontsConfig(Serializable):
    family: str = "Times New Roman"
    size: int = 34


class Arguments(Serializable):
    A: float = 5
    B: float = 1
    v_0: float = 0
    t_range: tuple[int, int] = (0, 20)


class Configuration(Serializable):
    fonts: FontsConfig = FontsConfig.get_default()
    plot_args: Arguments = Arguments.get_default()
    asymptote: bool = False
