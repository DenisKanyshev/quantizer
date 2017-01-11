# coding=utf-8
# https://en.wikipedia.org/wiki/Octree
from palette import Palette


class Octree(Palette):
    def __init__(self, pixel, distance_algorithm):
        super(Octree, self).__init__(distance_algorithm)
        pixel.connection.create_function("levind", 4, level_index)
        for rgb in quantization(pixel.cursor):
            self.append(rgb)


def level_index(red, green, blue, level):
    red, green, blue = int(red), int(green), int(blue)
    index = 0
    mask = 0b10000000 >> level
    if red & mask:
        index |= 4
    if green & mask:
        index |= 2
    if blue & mask:
        index |= 1
    return index


def quantization(cursor):
    cursor.execute(
        "CREATE TABLE cube AS "
        "SELECT red, green, blue, COUNT(*) AS total "
        "FROM pixel "
        "GROUP BY red, green, blue "
        "ORDER BY total DESC"
    )
    cursor.execute("SELECT COUNT(*) FROM cube")
    assert cursor.fetchone()[0] >= 256, "too few colors"
    cursor.execute(
        "CREATE TABLE indexes AS "
        "SELECT red, green, blue, total, "
        " levind(red, green, blue, 0) as i0, "
        " levind(red, green, blue, 1) as i1, "
        " levind(red, green, blue, 2) as i2, "
        " levind(red, green, blue, 3) as i3, "
        " levind(red, green, blue, 4) as i4, "
        " levind(red, green, blue, 5) as i5, "
        " levind(red, green, blue, 6) as i6, "
        " levind(red, green, blue, 7) as i7 "
        "FROM cube "
    )
    rows = ()
    for level in xrange(3, 9, 1):
        order = ",".join(("i%d" % _ for _ in xrange(level)))
        cursor.execute(
            "SELECT "
            " ROUND(SUM(red * total)/SUM(total)) AS red, "
            " ROUND(SUM(green * total)/SUM(total)) AS green, "
            " ROUND(SUM(blue * total)/SUM(total)) AS blue, "
            " SUM(total) as total "
            "FROM indexes "
            "GROUP BY %s "
            "ORDER BY total DESC "
            "LIMIT 256" % order
        )
        rows = cursor.fetchall()
        if len(rows) == 256:
            break
    for red, green, blue, _ in rows:
        yield red, green, blue
