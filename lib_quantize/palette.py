# coding=utf-8
# https://en.wikipedia.org/wiki/Median_cut
# http://algolist.manual.ru/graphics/find_col.php
import itertools
from . import r709


class Palette(list):
    def __init__(self, pixel):
        super(Palette, self).__init__()
        for rgb in mediana(pixel.cursor):
            self.append(rgb)
        self.chain = list(itertools.chain(*self))

    def match(self, color):
        # search for the best matching color in the palette
        diff = [difference(palette, color) for palette in self]
        return diff.index(min(diff))


def difference(palette, color):
    r = r709.RED_RATIO * ((palette[0] - color[0]) ** 2)
    g = r709.GREEN_RATIO * ((palette[1] - color[1]) ** 2)
    b = r709.BLUE_RATIO * ((palette[2] - color[2]) ** 2)
    return r + g + b


def mediana(cursor):
    cursor.execute(
        "CREATE TABLE cube AS "
        "SELECT red, green, blue, COUNT(*) AS total "
        "FROM pixel "
        "GROUP BY red, green, blue "
        "ORDER BY total DESC"
    )
    cursor.execute("SELECT COUNT(*) FROM cube")
    assert cursor.fetchone()[0] >= 256, "too few colors"
    cube = ["cube"]
    for _ in xrange(8):
        temp = []
        for segment in cube:
            temp += split_cube_segment(cursor, segment)
            cursor.execute("DROP TABLE %s" % segment)
        cube = temp
    for segment in cube:
        cursor.execute(
            "SELECT "
            " CAST(ROUND(SUM(red * total) / SUM(total)) AS INTEGER), "
            " CAST(ROUND(SUM(green * total) / SUM(total)) AS INTEGER), "
            " CAST(ROUND(SUM(blue * total) / SUM(total)) AS INTEGER) "
            "FROM %s" % segment
        )
        r, g, b = cursor.fetchone()
        cursor.execute("DROP TABLE %s" % segment)
        yield r, g, b


def split_cube_segment(cursor, segment):
    cursor.execute(
        "SELECT "
        " MAX(red) - MIN(red), "
        " MAX(green) - MIN(green), "
        " MAX(blue) - MIN(blue), "
        " COUNT(*) "
        "FROM %s" % segment
    )
    r, g, b, count = cursor.fetchone()
    r *= r709.RED_RATIO
    g *= r709.GREEN_RATIO
    b *= r709.BLUE_RATIO
    rgb = max(r, g, b)
    if rgb == g:
        order = "green, red, blue"
    elif rgb == r:
        order = "red, green, blue"
    else:
        order = "blue, green, red"
    center = count / 2
    segment_1 = "%s0" % segment
    cursor.execute(
        "CREATE TABLE {new_table_name} AS "
        "SELECT * FROM {table_name} "
        "ORDER BY {order} "
        "LIMIT {limit}".format(
            new_table_name=segment_1,
            table_name=segment,
            order=order,
            limit=center
        )
    )
    segment_2 = "%s1" % segment
    cursor.execute(
        "CREATE TABLE {new_table_name} AS "
        "SELECT * FROM {table_name} "
        "ORDER BY {order} "
        "LIMIT {limit} "
        "OFFSET {offset}".format(
            new_table_name=segment_2,
            table_name=segment,
            order=order,
            limit=count,
            offset=center
        )
    )
    return segment_1, segment_2
