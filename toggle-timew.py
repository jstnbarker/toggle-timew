#!/bin/python

import datetime
import os
import subprocess
import json

class entry():
    annotation: str
    taglist: list[str]
    start: datetime.datetime
    end: datetime.datetime

    def __init__(self, line: str):
        line = line.replace("\n", "")
        delimited = line.split(' # ')
        try:
            self.taglist = delimited[1].split(' ')
        except Exception:
            self.taglist = []
        try:
            self.annotation = delimited[2]
        except Exception:
            self.annotation = ""
        date_interval = delimited[0].split(' ')
        try:
            self.start = datetime.datetime.fromisoformat(date_interval[1])
            self.end = datetime.datetime.fromisoformat(date_interval[3])
        except IndexError:
            return

    def __str__(self):
        return "{0} -- {1}".format(self.annotation, " ".join(self.taglist))

    def duration(self):
        delta: datetime.timedelta
        try:
            delta = self.end - self.start
        except Exception:
            now = datetime.datetime.now(datetime.timezone.utc)
            delta = now - self.start
        return delta


def dmenu(options=[''], prompt="", vertical=1):
    options = "\n".join(options)
    dmenu_string = "dmenu "
    if len(prompt) != 0:
        dmenu_string += "-p '" + prompt + "' "
    if vertical != 1:
        dmenu_string += "-l " + str(vertical) + " "
    return subprocess.getoutput("printf '{0}' | {1}".format(options, dmenu_string))

def start_timew(annotation: str, taglist: list[str]):
    os.system("timew start " + " ".join(taglist))
    os.system("timew annotate '" + annotation + "'")

def main():
    config = json.loads(open("./config.json").read())
    now = datetime.datetime.now(datetime.timezone.utc)
    path = config["data_dir"] + str(now.year) + "-" + "{:02d}".format(now.month)+ ".data"

    entries = open(path, "r").readlines()
    entries.reverse()
    last = entry(entries[0])

    # exit code 0 means open interval
    # if interval started more than 3 minutes ago save; otherwise cancel
    if os.system("timew") == 0:
        if last.duration().seconds/60 > config["threshold"]:
            os.system("timew stop")
        else:
            os.system("timew cancel")
        os.system("pkill -RTMIN+" + str(config["signal"]) + " dwmblocks")
        return
    
    options = [str(last), "continue", "leetcode", "htb", "anime", "anki"]
    sel = dmenu(options=options, prompt="What doing?")
    if sel == str(last):
        os.system("timew continue @1")
    elif sel == "continue":
        entry_list = []
        added_hashes = []
        options_list = []
        for index in range(len(entries)):
            temp = entry(entries[index])
            if hash(str(temp)) not in added_hashes and len(added_hashes) < config["continue_limit"]:
                entry_list.append(temp)
                options_list.append(str(temp))
                added_hashes.append(hash(str(temp)))
        e = entry_list[options_list.index(dmenu(options_list,vertical=20))]
        start_timew(e.annotation, e.taglist)
    else:
        taglist = [sel]
        if sel == "anime":
            taglist.append("jp")
            taglist.append("immersion")
        elif sel == "anki":
            taglist.append("jp")
        elif sel == "leetcode":
            taglist.append("dev")
        annotation = dmenu(prompt="Annotation")
        start_timew(annotation, taglist)
    os.system("pkill -RTMIN+" + str(config["signal"]) + " dwmblocks")
    return 0


if __name__ == '__main__':
    main()
