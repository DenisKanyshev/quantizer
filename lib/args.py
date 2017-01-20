# coding=utf-8
import argparse


def arguments():
    parser = argparse.ArgumentParser(
        description="Color image quantization",
        epilog="Quantized image saved as "
               "{path}_quantized_"
               "({algorithm}_{distance}_{dithering}_{luma}).png"
    )
    parser.add_argument(
        "path",
        type=str,
        help="path to image file"
    )
    parser.add_argument(
        "-a",
        dest="algorithm",
        choices=["median-cut", "medain-cut-with-luma-correction", "octree"],
        default="median-cut",
        help="quantization algorithm, default: median-cut"
    )
    parser.add_argument(
        "-e",
        dest="distance",
        choices=["luma", "red-mean"],
        default="luma",
        help="euclidean distance algorithm, default: luma"
    )
    parser.add_argument(
        "-d",
        dest="dithering",
        choices=[
            "none", "floyd-steinberg", "jarvis-judice-and-ninke",
            "stucki", "atkinson", "burkes",
            "sierra", "two-row-sierra", "sierra-lite"
        ],
        default="floyd-steinberg",
        help="dithering algorithm, default: floyd-steinberg"
    )
    parser.add_argument(
        "--luma",
        action="store_true",
        help="use of relative luminance to correction dithering, "
             "default is False"
    )
    return parser.parse_args()
