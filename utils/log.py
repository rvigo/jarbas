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
        self.first_name = update.message.from_user.first_name
        self.timestamp = update.message.date.astimezone(timezone)
        self.text = update.message.text
        self.chat_type = update.message.chat.type
        self.chat_id = update.message.chat_id
        self.group_title = update.message.chat.title
        # log itself when created
        self.log()

    def log(self):
        get_log_collection().insert_one({'timestamp': self.timestamp, 'first_name': self.first_name, 'username': self.username, 'user_id': self.user_id,
                                         'chat_type': self.chat_type, 'title': self.group_title, 'text': self.text, 'chat_id': self.chat_id})
