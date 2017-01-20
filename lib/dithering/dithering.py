# coding=utf-8
# https://en.wikipedia.org/wiki/Dither
# http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/
from operator import sub, mul
from lib import luma
from lib.dithering import formulas


luma_correction = (
    1.0 / luma.GREEN * luma.RED,
    1.0,
    1.0 / luma.GREEN * luma.BLUE
)


def dithering(image, formula, use_luma=False):
    formula = formula.replace("-", "_")
    formula = getattr(formulas, formula, None)

    def wrapper(x, y, rgb):
        if formula is None:
            return
        error = map(sub, image[x, y], rgb)
        if use_luma:
            error = map(mul, error, luma_correction)
        for xd, yd, rate in formula:
            xd = xd + x
            yd = yd + y
            if not (0 <= xd < image.x and 0 <= yd < image.y):
                continue
            rgb = []
            for color, color_error in zip(image[xd, yd], error):
                color = color + color_error * rate
                if color < 0:
                    color = 0.0
                elif color > 255:
                    color = 255.0
                rgb.append(color)
            image[xd, yd] = rgb

    return wrapper
