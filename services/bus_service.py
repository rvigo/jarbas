from context.context import get_collection
from bisect import bisect_left
from datetime import datetime
import pytz

SP_TZ = pytz.timezone('America/Sao_Paulo')


def validate_request(tg_timestamp, args=[1]):
    """validate params before process the bus schedule"""
    try:
        rng = None
        if len(args) != 0:
            rng = int(args[0])
            if rng < 1:
                return f"{rng} não dá, né amigão..."
        else:
            rng = 1

        return get_next_departure(tg_timestamp, rng)
    except (TypeError, ValueError):
        return "o parametro tem que ser um número..."


def get_next_departure(tg_timestamp, lst_range):
    try:
        sp_time, noon = prepare_time(tg_timestamp)
        if sp_time.time() >= noon.time():
            id = 1
        else:
            id = 0

        result_lst = get_collection().find(
            {'_id': id}, {'_id': 0, 'sentido': 0})
        time_lst = list(result_lst)[0]['horarios']
        nearest_value = nearest_time(sp_time, time_lst)

        return next_items(lst_range, nearest_value, time_lst)

    except Exception as e:
        print(e)


def nearest_time(time, times):
    """find the next time base on telegram datetime"""
    pos = bisect_left(times, time)
    if pos == 0:
        return times[0]
    if pos == len(times):
        return times[-1]
    after = times[pos]

    return after

# rng = value range
def next_items(rng, time, times):
    """return "n" next itens in the datetime list based on "time" and "rng" params"""
    if(rng is 1):
        return time.strftime('%H:%M')
    idx = times.index(time)
    last_idx = idx + rng
    next_items_lst = [datetime.strftime(d, '%H:%M')
                      for d in times[idx: last_idx]]
    res = '\n'

    return res.join(next_items_lst)


def prepare_time(tg_timestamp):
    """convert telegram datetime to São Paulo timezone and then return a tuple with it and noon time (13h)"""
    sp_time = tg_timestamp.astimezone(SP_TZ).replace(
        year=1900, day=1, month=1, tzinfo=None)
    noon = datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)

    return sp_time, noon
