# quantizer
Color image quantization

Convert image from full color to palette (256 colors) with dithering

Required: Python 2.7, PIL/Pillow

# usage
```
.\quantizer>quantizer.py --help
usage: quantizer.py [-h]
                    [-a {median-cut,medain-cut-with-luma-correction,octree}]
                    [-e {luma,red-mean}]
                    [-d {none,floyd-steinberg,jarvis-judice-and-ninke,stucki,atkinson,burkes,sierra,two-row-sierra,sierra-lite}]
                    [--luma]
                    path

Color image quantization

positional arguments:
  path                  path to image file

optional arguments:
  -h, --help            show this help message and exit
  -a {median-cut,medain-cut-with-luma-correction,octree}
                        quantization algorithm, default: median-cut
  -e {luma,red-mean}    euclidean distance algorithm, default: luma
  -d {none,floyd-steinberg,jarvis-judice-and-ninke,stucki,atkinson,burkes,sierra,two-row-sierra,sierra-lite}
                        dithering algorithm, default: floyd-steinberg
  --luma                use of relative luminance to correction dithering,
                        default is False

Quantized image saved as
{path}_quantized_({algorithm}_{distance}_{dithering}_{luma}).png
```