#!/bin/python

from timew import *

import os
import subprocess
import json

def dmenu(dmenu="dmenu", options=[''], prompt="", vertical=0):
    options = "\n".join(options)
    dmenu_string = dmenu
    if len(prompt) != 0:
        dmenu_string += " -p '" + prompt + "' "
    if vertical != 0:
        dmenu_string += " -l " + str(vertical) + " "
    return subprocess.getoutput("printf '{0}' | {1}".format(options, dmenu_string))

def signal_process(signum, process_name):
    os.system("pkill -RTMIN+" + str(signum) + " " + process_name)

def readable(interval: entry):
    out = ""
    if interval.annotation != "":
        out += interval.annotation
    
    tags = " ".join(interval.taglist)
    if interval.annotation != "" and tags != "":
        out += " - "
    if tags != "":
        out += "["
        out += " ".join(interval.taglist)
        out += "]"
    return out

def main():
    config = json.loads(open("./config.json").read())
    intervals = get_intervals(config["data_dir"], quantity=1000)
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
    
    options = [readable(last), "continue", "leetcode", "htb", "anime", "anki"]
    sel = dmenu(dmenu=config["dmenu"], options=options, prompt="What doing?")
    if sel == "":
        return
    elif sel == readable(last):
        continue_interval(intervals[0])
    elif sel == "continue":
        unique = dict()
        for interval in intervals:
            key = readable(interval)
            if key != "":
                unique[key] = interval
        menu_result = dmenu(dmenu=config["dmenu"], options=list(unique.keys()), vertical=20)
        if menu_result != "":
            selection = unique[menu_result]
            continue_interval(selection)
        return
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
