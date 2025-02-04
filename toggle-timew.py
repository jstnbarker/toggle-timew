#!/bin/python

from timew import *

import os
from os import environ, system
import subprocess
import json
import argparse

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

dmenu_program=""
status_bar=""
signal=""

def main():
    arg = argparse.ArgumentParser(usage="Prompts user with all unique tag/annotation combinations from the last 1k intervals")
    arg.add_argument('--dmenu', help="dmenu-compatible program to prompt user")
    arg.add_argument('--bar', help="bar to send signal")
    arg.add_argument('--signal', help='RTMIN+n')

    config = json.loads(open(environ["HOME"] + "/.config/toggle-timew/config.json").read())
    dmenu_program = config["dmenu"]
    signal = config["signal"]
    status_bar = config["bar"]

    args = arg.parse_args()
    if args.dmenu is not None:
        dmenu_program = args.dmenu
    if args.bar:
        status_bar = args.bar
    if args.signal:
        signal = args.signal
    
    intervals = get_intervals(config["data_dir"], quantity=1000)
    last = intervals[0]

    # exit code 0 means open interval
    # if interval started more than `config['threshold']` minutes ago save; otherwise cancel
    if os.system("timew") == 0:
        if last.duration().seconds/60 > config["threshold"]:
            system("timew stop")
        else:
            system("timew cancel")
        signal_process(signal, status_bar)
        return

    # Find all unique combinations of tags and annotations
    unique = dict()
    for interval in intervals:
        key = readable(interval)
        if key != "":
            unique[key] = interval

    # Present unique choices to user
    menu_result = dmenu(dmenu=dmenu_program, options=list(unique.keys()), vertical=20)
    
    if menu_result != "":
        selection = unique[menu_result]
        continue_interval(selection)

    signal_process(signal, status_bar)
    return 0

if __name__ == '__main__':
    main()
