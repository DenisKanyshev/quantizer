# coding=utf-8
# https://en.wikipedia.org/wiki/Color_quantization
import os
import PIL.Image
from lib import arguments, ImageDB, progress_bar
from lib.dithering import dithering
from lib.palette import MedianCut, Octree


"""
def example():
    image = ImageDB("example.jpg")
    palette = MedianCut(image, "luma")
    new_image = PIL.Image.new("P", (image.x, image.y))
    new_image.putpalette(palette.chain)
    pixels = new_image.load()
    dith = dithering(image, "floyd-steinberg")
    for x, y, color in image:
        index = palette.match(color)
        pixels[x, y] = index
        dith(x, y, palette[index])
    new_image.save("example.png")
"""


def main(args):
    print "open image"
    image = ImageDB(args.path)
    print "create palette"
    if args.algorithm == "median-cut":
        palette = MedianCut(image, args.distance)
    elif args.algorithm == "medain-cut-with-luma-correction":
        palette = MedianCut(image, args.distance, True)
    else:
        palette = Octree(image, args.distance)
    print "quantization"
    new_image = PIL.Image.new("P", (image.x, image.y))
    new_image.putpalette(palette.chain)
    pixels = new_image.load()
    dith = dithering(image, args.dithering, args.luma)
    pb = progress_bar(len(image))
    for x, y, color in image:
        pb()
        index = palette.match(color)
        pixels[x, y] = index
        dith(x, y, palette[index])
    print "save image"
    path = "{name}_quantized_({algorithm}_{distance}_{dithering}{luma}).png"
    path = path.format(
        name=os.path.splitext(args.path)[0],
        algorithm=args.algorithm,
        distance=args.distance,
        dithering=args.dithering,
        luma="_luma" if args.luma and args.dithering != "none" else ""
    )
    new_image.save(path)


if __name__ == "__main__":
    main(arguments())
