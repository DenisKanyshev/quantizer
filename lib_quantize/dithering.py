# coding=utf-8
# https://en.wikipedia.org/wiki/Dither
# for more correction_table visit:
# http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/
from operator import sub, mul
from . import r709


ERROR_CORRECTION = (
    1.0 / r709.GREEN_RATIO * r709.RED_RATIO,
    1.0,
    1.0 / r709.GREEN_RATIO * r709.BLUE_RATIO
)


def dithering(pixel, x, y, color):
    # Floyd-Steinberg Dithering
    correction_table = (
        (x+1, y, 7.0/16),
        (x+1, y+1, 1.0/16),
        (x, y+1, 5.0/16),
        (x-1, y+1, 3.0/16)
    )
    error = map(sub, pixel[x, y], color)
    error = map(mul, error, ERROR_CORRECTION)
    for x, y, rate in correction_table:
        if not (0 <= x < pixel.X and 0 <= y < pixel.Y):
            continue
        rgb = []
        for value in zip(pixel[x, y], error):
            value = value[0] + value[1] * rate
            # value = 0.0 if value < 0 else 255.0 if value > 255 else value
            if value < 0:
                value = 0.0
            elif value > 255:
                value = 255.0
            rgb.append(value)
        pixel[x, y] = rgb
