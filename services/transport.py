from bisect import bisect_left
from datetime import datetime
import pytz

timezone = pytz.timezone('America/Sao_Paulo')


class Transport:
    '''interface for transport type classes'''

    def next_departure(self, tg_timestamp, lst_range):
        pass

    def validate_request(self, tg_timestamp, args=[1]):
        '''validate params before process the bus schedule'''
        try:
            rng = None
            if len(args) != 0:
                rng = int(args[0])
                if rng < 1:
                    return f'{rng} não dá, né amigão...'
            else:
                rng = 1

            return self.next_departure(tg_timestamp, rng)
        except (TypeError, ValueError):
            return 'o parametro tem que ser um número...'

    def nearest_time(self, time, times):
        '''find the next time base on telegram datetime'''
        pos = bisect_left(a=times, x=time, hi=len(times) - 1)
        if pos == 0:
            return times[0]
        if pos == len(times):
            return times[-1]
        after = times[pos]

        return after

    # rng = value range
    def next_items(self, rng, time, times):
        '''return 'n' next itens in the datetime list based on 'time' and 'rng' params'''
        if(rng is 1):
            return time.strftime('%H:%M')
        idx = times.index(time)
        last_idx = idx + rng
        next_items_lst = [datetime.strftime(d, '%H:%M')
                          for d in times[idx: last_idx]]
        res = '\n'

        return res.join(next_items_lst)

    def prepare_time(self, tg_timestamp):
        '''convert telegram datetime to São Paulo timezone'''
        sp_time = tg_timestamp.astimezone(timezone).replace(
            year=1900, day=1, month=1, tzinfo=None)
        
        return sp_time
