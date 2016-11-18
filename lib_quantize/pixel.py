# coding=utf-8
import os
import sqlite3


DB_NAME = "pixels.db"


class Pixel:
    def __init__(self, img):
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)
        self.__connection = sqlite3.connect(DB_NAME)
        self.cursor = self.__connection.cursor()
        self.cursor.execute(
            "CREATE TABLE pixel(red REAL, green REAL, blue REAL)"
        )
        self.cursor.executemany(
            "INSERT INTO pixel VALUES(?, ?, ?)",
            img.getdata()
        )
        self.X, self.Y = img.size

    def __getitem__(self, (x, y)):
        rowid = y * self.X + x + 1
        self.cursor.execute(
            "SELECT red, green, blue "
            "FROM pixel "
            "WHERE rowid = ?",
            (rowid,)
        )
        return self.cursor.fetchone()

    def __setitem__(self, (x, y), (r, g, b)):
        rowid = y * self.X + x + 1
        self.cursor.execute(
            "UPDATE pixel "
            "SET red = ?, green = ?, blue = ? "
            "WHERE rowid = ?",
            (r, g, b, rowid)
        )

    def __del__(self):
        self.__connection.close()
        os.remove(DB_NAME)
