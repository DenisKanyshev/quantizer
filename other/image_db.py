# coding=utf-8
import os
import sqlite3
import PIL.Image


class ImageDB:
    def __init__(self, path):
        img = PIL.Image.open(path)
        assert img.mode == "RGB", "image must be in RGB mode"
        self.__path = "%s.db" % os.path.splitext(path)[0]
        if os.path.exists(self.__path):
            os.remove(self.__path)
        self.connection = sqlite3.connect(self.__path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE pixel(red REAL, green REAL, blue REAL)"
        )
        self.cursor.executemany(
            "INSERT INTO pixel VALUES(?, ?, ?)",
            img.getdata()
        )
        self.x, self.y = img.size

    def __getitem__(self, (x, y)):
        rowid = y * self.x + x + 1
        self.cursor.execute(
            "SELECT red, green, blue "
            "FROM pixel "
            "WHERE rowid = ?",
            (rowid,)
        )
        return self.cursor.fetchone()

    def __setitem__(self, (x, y), (red, green, blue)):
        rowid = y * self.x + x + 1
        self.cursor.execute(
            "UPDATE pixel "
            "SET red = ?, green = ?, blue = ? "
            "WHERE rowid = ?",
            (red, green, blue, rowid)
        )

    def __iter__(self):
        for y in xrange(self.y):
            for x in xrange(self.x):
                color = self[x, y]
                yield x, y, color

    def __len__(self):
        return self.x * self.y

    def __del__(self):
        self.connection.close()
        os.remove(self.__path)
