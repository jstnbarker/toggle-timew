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
            self.annotation = delimited[2].strip('"')
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

def dmenu(dmenu="dmenu", options=[''], prompt="", vertical=0):
    options = "\n".join(options)
    dmenu_string = dmenu
    if len(prompt) != 0:
        dmenu_string += " -p '" + prompt + "' "
    if vertical != 0:
        dmenu_string += " -l " + str(vertical) + " "
    return subprocess.getoutput("printf '{0}' | {1}".format(options, dmenu_string))

def start_timew(annotation: str, taglist: list[str]):
    os.system("timew start " + " ".join(taglist))
    os.system("timew annotate '" + annotation + "'")

def signal_process(signum, process_name):
    os.system("pkill -RTMIN+" + str(signum) + " " + process_name)

def get_intervals(path, quantity=10):
    now = datetime.datetime.now(datetime.timezone.utc)
    entries = []
    month = now.month
    year = now.year
    current_count = 0
    while(True):
        month -= 1
        if month <= 0:
            month += 12
            year -= 1
        if year < 1970: 
            return [] 
        path = path + str(year) + "-" + "{:02d}".format(month)+ ".data"
        try:
            data = open(path, "r")
            temp = data.readlines()
            data.close()
            temp.reverse()
            for line in temp:
                entries.append(entry(line))
                current_count += 1
                if current_count == quantity:
                    return entries
                
        except FileNotFoundError:
            pass

def main():
    config = json.loads(open("./config.json").read())

    intervals = get_intervals(config["data_dir"], quantity=100)

    last = intervals[0]
    # exit code 0 means open interval
    # if interval started more than `config['threshold']` minutes ago save; otherwise cancel
    if os.system("timew") == 0:
        if last.duration().seconds/60 > config["threshold"]:
            os.system("timew stop")
        else:
            os.system("timew cancel")
        signal_process(config["signal"], config["bar"])
        return
    
    options = [str(last), "continue", "leetcode", "htb", "anime", "anki"]
    sel = dmenu(dmenu=config["dmenu"], options=options, prompt="What doing?")
    if sel == "":
        return
    elif sel == str(last):
        os.system("timew continue @1")
    elif sel == "continue":
        unique = dict()
        for interval in intervals:
            key = str(interval)
            try: 
                unique[key]
            except KeyError:
                unique[key] = interval
        selection = unique[dmenu(dmenu=config["dmenu"], options=list(unique.keys()), vertical=20)]
        start_timew(taglist=selection .taglist, annotation=selection.annotation)
    else:
        taglist = [sel]
        if sel == "anime":
            taglist.append("jp")
            taglist.append("immersion")
        elif sel == "anki":
            taglist.append("jp")
        elif sel == "leetcode":
            taglist.append("dev")
        annotation = dmenu(dmenu=config["dmenu"] ,prompt="Annotation")
        start_timew(annotation, taglist)
    signal_process(config["signal"], config["bar"])
    return 0

if __name__ == '__main__':
    main()
