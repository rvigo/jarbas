from functools import wraps
from utils import log
import os

LIST_OF_ADMINS = [os.environ['ADMIN']]

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.message.from_user.id
        if user_id not in LIST_OF_ADMINS:
            log.debug(f'Unauthorized access denied for {user_id}.')
            return
        return func(bot, update, *args, **kwargs)
    return wrapped