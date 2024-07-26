import datetime


def subtract_datetimes(time: datetime.time, period: datetime.timedelta):
    return (datetime.datetime.combine(datetime.datetime.today(), time) - period).time()


def add_datetimes(time: datetime.time, period: datetime.timedelta):
    return (datetime.datetime.combine(datetime.datetime.today(), time) + period).time()
