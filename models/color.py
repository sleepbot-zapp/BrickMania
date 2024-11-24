import typing

ColorType = typing.Tuple[int, int, int]


class Color:
    BLACK = (32, 32, 45)
    BLUE = (137, 180, 250)
    GREEN = (142, 227, 131)
    GREY = (92, 95, 119)
    RED = (232, 134, 135)
    WHITE = (227, 231, 255)
    YELLOW = (249, 226, 175)

    def __init__(
        self,
        BLACK=None,
        BLUE=None,
        GREEN=None,
        GREY=None,
        RED=None,
        WHITE=None,
        YELLOW=None,
    ) -> None:
        self.BLACK: ColorType = BLACK or (32, 32, 45)
        self.BLUE: ColorType = BLUE or (137, 180, 250)
        self.GREEN: ColorType = GREEN or (142, 227, 131)
        self.GREY: ColorType = GREY or (92, 95, 119)
        self.RED: ColorType = RED or (232, 134, 135)
        self.WHITE: ColorType = WHITE or (227, 231, 255)
        self.YELLOW: ColorType = YELLOW or (249, 226, 175)
