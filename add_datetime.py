import datetime


def subtract_datetimes(time: datetime.time, period: datetime.timedelta):
    return (datetime.datetime.combine(datetime.datetime.today(), time) - period).time()


def add_datetimes(time: datetime.time, period: datetime.timedelta):
    return (datetime.datetime.combine(datetime.datetime.today(), time) + period).time()


def map_datetime_to_value(time: datetime.time, time_min: datetime.time, time_max: datetime.time, new_min: float, new_max: float):
    if time > time_max:
        return new_max
    elif time < time_min:
        return new_min
    return new_min + ((time_to_seconds(time) - time_to_seconds(time_min) * (new_max - new_min)) / (time_to_seconds(time_max) - time_to_seconds(time_min)))

def time_to_seconds(time: datetime.time) -> int:
    return time.hour * 3600 + time.minute * 60 + time.second

def seconds_to_time(total_seconds: int) -> datetime.time:
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Create a time object
    return datetime.time(hours, minutes, seconds)