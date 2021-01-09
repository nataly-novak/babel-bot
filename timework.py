import pytz
import datetime


def toUTC(date, time, zone):
    local_time = pytz.timezone(zone.rstrip())
    line = date + " " + time+":00"
    naive_datetime = datetime.datetime.strptime(line, "%Y-%m-%d %H:%M:%S")
    local_datetime = local_time.localize(naive_datetime, is_dst=None)
    utc_datetime = local_datetime.astimezone(pytz.utc)
    conversion = str(utc_datetime).split(sep="+")[0]+" UTC"
    return conversion


