# coding=utf-8
# https://en.wikipedia.org/wiki/Euclidean_distance
# http://algolist.manual.ru/graphics/find_col.php
# http://www.compuphase.com/cmetric.htm
from lib.luma import RED, GREEN, BLUE


class Palette(list):
    def __init__(self, distance_algorithm):
        super(Palette, self).__init__()
        if distance_algorithm == "luma":
            self.match = self.__distance_luma
        else:
            self.match = self.__distance_red_mean

    def __distance_luma(self, (r, g, b)):
        """
        use Euclidean distance
        to find the best color matching in the palette
        """
        minimum = float("inf")
        minimum_index = 0
        index = 0
        for red, green, blue in self:
            red = red - r
            green = green - g
            blue = blue - b
            red = red * red * RED
            green = green * green * GREEN
            blue = blue * blue * BLUE
            rgb = red + green + blue
            if rgb < minimum:
                minimum = rgb
                minimum_index = index
            index += 1
        return minimum_index

    def __distance_red_mean(self, (r, g, b)):
        minimum = float("inf")
        minimum_index = 0
        index = 0
        for red, green, blue in self:
            rmean = (red + r) / 2.0
            red = red - r
            green = green - g
            blue = blue - b
            red = red * red * (2.0 + rmean / 256.0)
            green = green * green * 4.0
            blue = blue * blue * (2.0 + (255.0 - rmean) / 256.0)
            rgb = red + green + blue
            if rgb < minimum:
                minimum = rgb
                minimum_index = index
            index += 1
        return minimum_index

    @property
    def chain(self):
        result = []
        for rgb in self:
            rgb = map(int, rgb)
            result.extend(rgb)
        return result
