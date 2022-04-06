from enum import Enum


class Count(Enum):
    ONE = 1
    TWO = 2
    THREE = 3


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Shade(Enum):
    SOLID = 1
    STRIPED = 2
    OPEN = 3


class Shape(Enum):
    TRIANGULAR = 1
    CIRCLE = 2
    WAVE = 3


class Card:
    def __init__(self, count, shape, shading, color, path) -> None:
        self.count = count
        self.shape = shape
        self.shading = shading
        self.color = color
        self.path_2_image = path

    def __eq__(self, other):
        return self.count == other.count and self.shape == other.shape and \
               self.shading == other.shading and self.color == other.color and \
               self.path_2_image == other.path_2_image
