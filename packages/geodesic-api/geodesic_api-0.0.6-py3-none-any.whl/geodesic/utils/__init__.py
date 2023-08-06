import datetime
import pytz


def is_offset_aware(t: datetime.datetime):
    '''
    Returns True if input is offset aware, False otherwise
    '''
    if t.tzinfo is not None and t.tzinfo.utcoffset(t) is not None:
        return True
    return False


def datetime_to_utc(d: datetime.datetime):
    '''
    Ensures input is localized UTC
    '''

    if is_offset_aware(d):
        return d.astimezone(pytz.UTC)

    return pytz.UTC.localize(d)
