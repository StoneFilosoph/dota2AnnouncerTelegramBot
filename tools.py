import datetime,pytz


debug = 0

"""
на вход какая-то строка и(или) datetime object  + какой часовой пояс/временная зона.
на выходе timestamp unix UTC  time
"""


def unix_timestamp (timestring_or_datetime_object,timezone):
    """from ordinary time to unix timestamp(UTC)


    :param timestring_or_datetime_object: string or datetime object (need preformation to view %Y-%m-%d %H:%M:%S)
    :param timezone: timezone name from 'pytz' library
    :return: unix timestamp number from given string time or datetime object
    """
    convert = datetime.datetime.strptime(timestring_or_datetime_object,'%Y-%m-%d %H:%M:%S')
    tzone = pytz.timezone(timezone)
    convert2 = convert.replace(tzinfo=tzone).astimezone(tz=pytz.utc)
    convert_timestamp = convert2.timestamp()
    return convert_timestamp


def zone_from_timestamp(stamp,zone='UTC'):
    """from unix timestamp to UTC time

    :param stamp: unix timestamp number
    :return: UTC timezone time preformated like %Y-%m-%d %H:%M:%S
    """
    from_timestamp = datetime.datetime.fromtimestamp(float(stamp)).strftime('%Y-%m-%d %H:%M:%S')
    tzone = pytz.timezone(zone)
    convert = datetime.datetime.strptime(from_timestamp,'%Y-%m-%d %H:%M:%S')
    convert2 = convert.replace(tzinfo=pytz.timezone('Etc/GMT')).astimezone(tz=tzone)
    return convert2.strftime('%Y-%m-%d %H:%M:%S')
