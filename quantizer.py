# coding=utf-8
# https://en.wikipedia.org/wiki/Color_quantization
import os
import sys
import PIL.Image
from lib_quantize import Pixel
from lib_quantize import Palette
from lib_quantize import dithering


def main(path):
    print "open image"
    img = PIL.Image.open(path)
    assert img.mode == "RGB", "image must be in RGB mode"
    pixel = Pixel(img)
    img = PIL.Image.new("P", img.size)
    print "create palette"
    palette = Palette(pixel)
    img.putpalette(palette.chain)
    print "quantize"
    indexed_pixel = img.load()
    for y in xrange(pixel.Y):
        sys.stdout.write("\r%d %%" % round(y / (pixel.Y / 100.0)))
        for x in xrange(pixel.X):
            index = palette.match(pixel[x, y])
            indexed_pixel[x, y] = index
            dithering(pixel, x, y, palette[index])
    print
    print "ok, save"
    # path = "%s_quantized.png" % os.path.splitext(path)[0]
    path = "%s_quantized.gif" % os.path.splitext(path)[0]
    img.save(path)


if __name__ == "__main__":
    main(sys.argv[1])
