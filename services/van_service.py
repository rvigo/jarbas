from context.context import get_ceic_collection
from services.transport import Transport
from utils import log


class VanService(Transport):
    def next_departure(self, tg_timestamp, lst_range):
        try:
            go_lst = get_ceic_collection().find(
                {'_id': 1}, {'_id': 0, 'sentido': 0})
            go_lst = list(go_lst)[0]['horarios']

            back_lst = get_ceic_collection().find(
                {'_id': 0}, {'_id': 0, 'sentido': 0})
            back_lst = list(back_lst)[0]['horarios']

            sp_time = self.prepare_time(tg_timestamp)

            go_nearest_value = self.nearest_time(sp_time, go_lst)
            back_nearest_value = self.nearest_time(sp_time, back_lst)

            go_res = self.next_items(lst_range, go_nearest_value, go_lst)
            back_res = self.next_items(lst_range, back_nearest_value, back_lst)
            
            return f'CT > CEIC:\n{go_res}\nCEIC > CT:\n{back_res}'

        except Exception as e:
            log.error(e.message, e)