#!/bin/python

import datetime


class entry():
    annotation = ""
    taglist = []
    start: datetime
    end: datetime

    def __init__(self, line: str):
        line = line.replace("\n", "")
        delimited = line.split('#')

        # build taglist
        try:
            self.taglist = delimited[1].split(' ')
        except Exception:
            print("No tags")
            print(line)
        # extract annotation
        try:
            self.annotation = delimited[2]
        except Exception:
            print("No annotation")
            print(line)
        # extract datetime interval
        date_interval = delimited[0].split(' ')
        self.start = datetime.datetime.fromisoformat(date_interval[1])
        self.end = datetime.datetime.fromisoformat(date_interval[3])

    def __str__(self):
        return "Annotation: {0}\nTaglist: {1}\nStart: {2}\nEnd: {3}".format(
                self.annotation, self.taglist, self.start, self.end)


def main():
    path = "/home/jstn/2024-04.data"
    entry_list = []
    for line in open(path, "r").readlines():
        entry_list.append(entry(line))
    return 0


if __name__ == '__main__':
    main()
