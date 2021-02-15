import pytz
import datetime
from timework import currentUTC

def print_stamp(stamp: datetime.datetime):
    return  str(stamp).rsplit(sep=":",maxsplit=1)[0]+";"

def line_stamp(line):
    if line != "":
        stamp = datetime.datetime.strptime(line, "%Y-%m-%d %H:%M")
        return stamp
    else:
        return None

def more_then_day(stamp1: datetime.datetime, stamp2:datetime.datetime):
    delta = datetime.timedelta(days=1)
    d = stamp1 - delta
    return d > stamp2

def stamp_list(line: str):
    return list(map(line_stamp, line.rstrip(";").split(sep=";")))

def stamp_print(lst):
    line = ""
    for i in lst:
        line = line+print_stamp(i)
    return line

def list_update(lst):
    new_stamp = datetime.datetime.strptime(currentUTC(), "%Y-%m-%d %H:%M")
    new_lst = []
    for i in lst:
        if not more_then_day(new_stamp, i):
            new_lst.append(i)
    new_lst.append(new_stamp)
    return new_lst

def line_update(line):
    if stamp_list(line) != [None]:
        return stamp_print(list_update(stamp_list(line)))
    else:
        return currentUTC()+";"
