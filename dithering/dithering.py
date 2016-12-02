# coding=utf-8
# https://en.wikipedia.org/wiki/Dither
# http://www.tannerhelland.com/4660/dithering-eleven-algorithms-source-code/
from operator import sub, mul, add
from other import luma
from .formula import *


luma_correction = (
    1.0 / luma.GREEN * luma.RED,
    1.0,
    1.0 / luma.GREEN * luma.BLUE
)


class Dithering(object):
    def __init__(self, pixel, formula, use_luma=False):
        self.__pixel = pixel
        self.__use_luma = use_luma
        if formula == "floyd-steinberg":
            self.__formula = floyd_steinberg
        elif formula == "jarvis-judice-and-ninke":
            self.__formula = jarvis_judice_and_ninke
        elif formula == "stucki":
            self.__formula = stucki
        elif formula == "atkinson":
            self.__formula = atkinson
        elif formula == "burkes":
            self.__formula = burkes
        elif formula == "sierra":
            self.__formula = sierra
        elif formula == "two-row-sierra":
            self.__formula = two_row_sierra
        elif formula == "sierra-lite":
            self.__formula = sierra_lite
        else:
            self.__formula = None

    def __call__(self, x, y, color):
        if self.__formula is None:
            return
        error = map(sub, self.__pixel[x, y], color)
        if self.__use_luma:
            error = map(mul, error, luma_correction)
        coordinates = (x, y, 0)
        for row in self.__formula:
            x, y, rate = map(add, coordinates, row)
            if not (0 <= x < self.__pixel.X and 0 <= y < self.__pixel.Y):
                continue
            rgb = []
            for value in zip(self.__pixel[x, y], error):
                value = value[0] + value[1] * rate
                # value = 0.0 if value < 0 else 255.0 if value > 255 else value
                if value < 0:
                    value = 0.0
                elif value > 255:
                    value = 255.0
                rgb.append(value)
            self.__pixel[x, y] = rgb
