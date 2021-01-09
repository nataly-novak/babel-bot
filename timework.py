import pytz
import datetime


def toUTC(date, time, zone):
    local_time = pytz.timezone(zone.rstrip())
    line = date + " " + time+":00"
    naive_datetime = datetime.datetime.strptime(line, "%Y-%m-%d %H:%M:%S")
    local_datetime = local_time.localize(naive_datetime, is_dst=None)
    utc_datetime = local_datetime.astimezone(pytz.utc)
    conversion = (str(utc_datetime).split(sep="+")[0]).rsplit(sep=":",maxsplit=1)[0]+" UTC"
    return conversion


def currentUTC():
    current = str(datetime.datetime.utcnow())
    current = current.split(sep=".")[0]
    current = current.rsplit(sep=":",maxsplit=1)[0]
    return current

def toLocal(date, time, zone):
    local_time = pytz.timezone(zone.rstrip())
    utc_time = pytz.timezone("UTC")
    line = date + " " + time+":00"
    naive_datetime = datetime.datetime.strptime(line, "%Y-%m-%d %H:%M:%S")
    utc_datetime = utc_time.localize(naive_datetime, is_dst=None)
    local_datetime = utc_datetime.astimezone(local_time)
    conversion = str((local_datetime).split(sep="+")[0]).rsplit(sep=":",maxsplit=1)[0]+" "+ zone
    return conversion







