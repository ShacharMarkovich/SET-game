from enum import Enum


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
