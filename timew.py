from datetime import datetime, timedelta, timezone
import os

class entry():
    annotation: str
    taglist: list[str]
    start: datetime
    end: datetime

    def __init__(self, line: str):
        line = line.replace("\n", "")
        segments= line.split(' # ')
        try:
            self.taglist = segments[1].split(' ')
        except Exception:
            self.taglist = []
        try:
            self.annotation = segments[2].strip('"')
        except Exception:
            self.annotation = ""

        date_interval = segments[0].split(' ')
        try:
            self.start = datetime.fromisoformat(date_interval[1])
            self.end = datetime.fromisoformat(date_interval[3])
        except IndexError:
            return

    def __str__(self):
        out = "inc "
        out += self.start.isoformat() + " - "
        out += self.end.isoformat()

        tags = " ".join(self.taglist)
        if tags != "":
            out += " # "
            out += tags

        if self.annotation != "":
            out += " # \"" + self.annotation + "\""
        
        return out

    def duration(self):
        delta: timedelta
        try:
            delta = self.end - self.start
        except Exception:
            now = datetime.now(timezone.utc)
            delta = now - self.start
        return delta

def get_intervals(path, quantity=10):
    now = datetime.now()
    entries = []
    month = now.month
    year = now.year
    current_count = 0
    while(True):
        try:
            data = open(path + str(year) + "-" + "{:02d}".format(month)+ ".data", "r")
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

        month -= 1
        if month <= 0:
            month += 12
            year -= 1
        if year < 1970: 
            return entries 

def start_timew(annotation: str, taglist: list[str]):
    os.system("timew start");
    if len(taglist) != 0:
        os.system("timew retag @1 " + " ".join(taglist))
    if annotation != "":
        os.system("timew annotate '" + annotation + "'")

def continue_interval(interval: entry):
    start_timew(interval.annotation, interval.taglist)

