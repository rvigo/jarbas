from context.context import get_ct_collection
from services.transport import Transport
from datetime import datetime


class BusService(Transport):

    def next_departure(self, tg_timestamp, lst_range):
        try:
            noon = datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)
            sp_time = self.prepare_time(tg_timestamp)
            if sp_time.time() >= noon.time():
                id = 1
            else:
                id = 0

            result_lst = get_ct_collection().find(
                {'_id': id}, {'_id': 0, 'sentido': 0})
            time_lst = list(result_lst)[0]['horarios']
            nearest_value = self.nearest_time(sp_time, time_lst)

            return self.next_items(lst_range, nearest_value, time_lst)

        except Exception as e:
            print(e)