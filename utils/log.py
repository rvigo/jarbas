from functools import wraps
from context.context import get_log_collection
import pytz

timezone = pytz.timezone('America/Sao_Paulo')

# log decorator
def log(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        try:
            Log(update)
        except Exception as e:
            print(f'ocorreu um erro ao logar: {e}')

        return func(bot, update, *args, **kwargs)
    return wrapped


class Log:
    '''custom object to log 'update' requests'''

    def __init__(self, update):
        self.username = update.message.from_user.username
        self.user_id = update.message.from_user.id
        self.timestamp = update.message.date.astimezone(timezone)
        self.text = update.message.text
        self.chat_id = update.message.chat_id
        # log itself when created
        self.log()

    def log(self):
        get_log_collection().insert_one({'username': self.username, 'user_id': self.user_id,
                                         'timestamp': self.timestamp, 'text': self.text, 'chat_id': self.chat_id})
