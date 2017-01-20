# coding=utf-8
import sys


def progress_bar(total):
    percentage = total / 100.0
    counter = {"percent": 0, "step": 0}

    def step():
        if counter["percent"] == 100:
            return
        percent = round(counter["step"] / percentage)
        if percent != counter["percent"]:
            counter["percent"] = percent
            sys.stdout.write("\r%3d %%" % percent)
            if percent == 100:
                sys.stdout.write("\n")
            sys.stdout.flush()
        counter["step"] += 1

    return step
