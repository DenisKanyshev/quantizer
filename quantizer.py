# coding=utf-8
# https://en.wikipedia.org/wiki/Color_quantization
import os
import sys
import PIL.Image
from dithering import Dithering
from other import arguments
from other import ImageDB
from palette import MedianCut, Octree


def main(args):
    print "open image"
    image_db = ImageDB(args.path)
    print "create palette"
    if args.algorithm == "median-cut":
        palette = MedianCut(image_db, args.distance)
    elif args.algorithm == "medain-cut-with-luma-correction":
        palette = MedianCut(image_db, args.distance, True)
    else:
        palette = Octree(image_db, args.distance)
    print "quantization"
    new_image = PIL.Image.new("P", (image_db.X, image_db.Y))
    new_image.putpalette(palette.chain)
    pixels = new_image.load()
    dithering = Dithering(image_db, args.dithering, args.luma)
    for y in xrange(image_db.Y):
        sys.stdout.write("\r%d %%" % round(y / (image_db.Y / 100.0)))
        sys.stdout.flush()
        for x in xrange(image_db.X):
            index = palette.match(image_db[x, y])
            pixels[x, y] = index
            dithering(x, y, palette[index])
    print "\nsave image"
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
