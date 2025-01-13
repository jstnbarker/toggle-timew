#!/bin/python

from timew import *

import os
from os import environ, system
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
        out += tags
        out += "]"
    return out

def main():
    config = json.loads(open(environ["HOME"] + "/.config/toggle-timew/config.json").read())
    intervals = get_intervals(config["data_dir"], quantity=1000)
    last = intervals[0]

    # exit code 0 means open interval
    # if interval started more than `config['threshold']` minutes ago save; otherwise cancel
    if os.system("timew") == 0:
        if last.duration().seconds/60 > config["threshold"]:
            system("timew stop")
        else:
            system("timew cancel")
        signal_process(config["signal"], config["bar"])
        return

    # Find all unique combinations of tags and annotations
    unique = dict()
    for interval in intervals:
        key = readable(interval)
        if key != "":
            unique[key] = interval

    # Present unique choices to user
    menu_result = dmenu(dmenu=config["dmenu"], options=list(unique.keys()), vertical=20)
    
    if menu_result != "":
        selection = unique[menu_result]
        continue_interval(selection)

    signal_process(config["signal"], config["bar"])
    return 0

if __name__ == '__main__':
    main()
