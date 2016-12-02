# coding=utf-8
# https://en.wikipedia.org/wiki/Euclidean_distance
# http://algolist.manual.ru/graphics/find_col.php
# http://www.compuphase.com/cmetric.htm
from itertools import chain
from other import luma


class Palette(list):
    def __init__(self, distance_algorithm):
        super(Palette, self).__init__()
        if distance_algorithm == "luma":
            self.__distance = distance_luma
        else:
            self.__distance = distance_red_mean

    def match(self, color):
        # use Euclidean distance to find the best color matching in the palette
        distances = [self.__distance(palette, color) for palette in self]
        return distances.index(min(distances))

    @property
    def chain(self):
        return list(chain.from_iterable(self))


# "x = x ** 2" is slower "x = x * x"
# "x *= x" is slower "x = x * x"
# "map(float, rgb)" is slower "rgb[0] * 1.0"
# the square root is meaningless


def distance_luma(rgb1, rgb2):
    r = rgb1[0] - rgb2[0]
    g = rgb1[1] - rgb2[1]
    b = rgb1[2] - rgb2[2]
    r = r * r * luma.RED
    g = g * g * luma.GREEN
    b = b * b * luma.BLUE
    return r + g + b


def distance_red_mean(rgb1, rgb2):
    rmean = (rgb1[0] + rgb2[0]) / 2.0
    r = rgb1[0] - rgb2[0] * 1.0
    g = rgb1[1] - rgb2[1] * 1.0
    b = rgb1[2] - rgb2[2] * 1.0
    r = r * r * (2 + rmean / 256)
    g = g * g * 4
    b = b * b * (2 + (255 - rmean) / 256)
    return r + g + b


"""
def distance_red_mean(rgb1, rgb2):
    # faster, but less accurate
    rmean = (rgb1[0] + rgb2[0]) / 2
    r = rgb1[0] - rgb2[0]
    g = rgb1[1] - rgb2[1]
    b = rgb1[2] - rgb2[2]
    r = (((512 + rmean) * r * r) >> 8)
    g = g * g * 4
    b = (((767 - rmean) * b * b) >> 8)
    return r + g + b
"""
