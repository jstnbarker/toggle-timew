#!/bin/python

import datetime
import sys
import os
import subprocess


class entry():
    annotation: str
    taglist: list[str]
    start: datetime
    end: datetime

    def __init__(self, line: str):
        line = line.replace("\n", "")
        delimited = line.split('#')

        # build taglist
        try:
            self.taglist = delimited[1].split(' ')
            self.taglist.pop(0)
            self.taglist.pop(len(self.taglist)-1)
        except Exception:
            self.taglist = []
        # extract annotation
        try:
            self.annotation = delimited[2]
        except Exception:
            self.annotation = ""
        # extract datetime interval
        date_interval = delimited[0].split(' ')
        self.start = datetime.datetime.fromisoformat(date_interval[1])
        self.end = datetime.datetime.fromisoformat(date_interval[3])

    def __str__(self):
        return "{0} -- {1}".format(self.annotation, " ".join(self.taglist))

    def duration(self):
        return self.end - self.start


def dmenu(options: list[str], prompt="", vertical=1):
    options = "\n".join(options)
    dmenu_string = "dmenu "
    if len(prompt) != 0:
        dmenu_string += "-p '" + prompt + "' "
    if vertical != 1:
        dmenu_string += "-l " + str(vertical) + " "
    return subprocess.getoutput("printf '{0}' | {1}".format(options, dmenu_string))


def main():
    path = "/home/jstn/2024-04.data"
    entries = open(path, "r").readlines()
    entries.reverse()
    last = entry(entries[0])
    options = [str(last), "continue", "leetcode", "htb", "jp"]

    sel = dmenu(options, prompt="What doing?")
    if sel == str(last):
        os.system("timew continue @1")
    elif sel == "continue":
        entry_list = []
        added_annotations = []
        options_list = []
        unique = 0
        for index in range(len(entries)):
            delim = entries[index].split("#")
            annotation = delim[len(delim)-1]
            if annotation not in added_annotations and unique < 20:
                entry_list.append(entry(entries[index]))
                options_list.append(str(entry_list[len(entry_list)-1]))
                added_annotations.append(annotation)
                unique += 1
        e = entry_list[options_list.index(dmenu(options_list,vertical=20))]
        print(e)
        return
    elif sel in options:
        return
    else:
        return
    os.system("pkill -RTMIN+9 dwmblocks")
    return 0


if __name__ == '__main__':
    main()
