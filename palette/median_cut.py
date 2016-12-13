# coding=utf-8
# https://en.wikipedia.org/wiki/Median_cut
from other import luma
from palette import Palette


class MedianCut(Palette):
    def __init__(self, pixel, distance_algorithm, use_luma=False):
        super(MedianCut, self).__init__(distance_algorithm)
        for rgb in quantization(pixel.cursor, use_luma):
            self.append(rgb)


def quantization(cursor, use_luma):
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
            temp += split_cube_segment(cursor, segment, use_luma)
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


def split_cube_segment(cursor, segment, use_luma):
    cursor.execute(
        "SELECT "
        " MAX(red) - MIN(red), "
        " MAX(green) - MIN(green), "
        " MAX(blue) - MIN(blue), "
        " COUNT(*) "
        "FROM %s" % segment
    )
    r, g, b, count = cursor.fetchone()
    if use_luma:
        r *= luma.RED
        g *= luma.GREEN
        b *= luma.BLUE
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
