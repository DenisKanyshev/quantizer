# coding=utf-8
# https://en.wikipedia.org/wiki/Euclidean_distance
# http://algolist.manual.ru/graphics/find_col.php
# http://www.compuphase.com/cmetric.htm
from itertools import chain
from other.luma import RED, GREEN, BLUE


class Palette(list):
    def __init__(self, distance_algorithm):
        super(Palette, self).__init__()
        if distance_algorithm == "luma":
            self.__distance = distance_luma
        else:
            self.__distance = distance_red_mean

    def match(self, color):
        """
        use Euclidean distance
        to find the best color matching in the palette
        """
        distance = self.__distance
        distances = [distance(palette, color) for palette in self]
        return distances.index(min(distances))

    @property
    def chain(self):
        return list(chain.from_iterable(self))


def distance_luma((r1, g1, b1), (r2, g2, b2)):
    r = r1 - r2
    g = g1 - g2
    b = b1 - b2
    r = r * r * RED
    g = g * g * GREEN
    b = b * b * BLUE
    return r + g + b


def distance_red_mean((r1, g1, b1), (r2, g2, b2)):
    rmean = (r1 + r2) / 2.0
    r = (r1 - r2) * 1.0
    g = (g1 - g2) * 1.0
    b = (b1 - b2) * 1.0
    r = r * r * (2.0 + rmean / 256.0)
    g = g * g * 4.0
    b = b * b * (2.0 + (255.0 - rmean) / 256.0)
    return r + g + b
