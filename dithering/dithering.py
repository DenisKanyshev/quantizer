# coding=utf-8
# https://en.wikipedia.org/wiki/Dither
# http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/
from operator import sub, mul
from other import luma
import formulas


luma_correction = (
    1.0 / luma.GREEN * luma.RED,
    1.0,
    1.0 / luma.GREEN * luma.BLUE
)


class Dithering(object):
    def __init__(self, image, formula, use_luma=False):
        self.__image = image
        self.__use_luma = use_luma
        formula = formula.replace("-", "_")
        self.__formula = getattr(formulas, formula, None)

    def __call__(self, x, y, rgb):
        if self.__formula is None:
            return
        error = map(sub, self.__image[x, y], rgb)
        if self.__use_luma:
            error = map(mul, error, luma_correction)
        for xd, yd, rate in self.__formula:
            xd = xd + x
            yd = yd + y
            if not (0 <= xd < self.__image.x and 0 <= yd < self.__image.y):
                continue
            rgb = []
            for color, color_error in zip(self.__image[xd, yd], error):
                color = color + color_error * rate
                if color < 0:
                    color = 0.0
                elif color > 255:
                    color = 255.0
                rgb.append(color)
            self.__image[xd, yd] = rgb
