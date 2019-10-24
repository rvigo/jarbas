from functools import wraps
from context.context import get_log_collection
import logging
import os
import pytz

timezone = pytz.timezone('America/Sao_Paulo')

# logging configs
logging.basicConfig(format='%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=os.environ['LOG_LEVEL'])


def log_decorator(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        try:
            log_update(update)
        except Exception as e:
            log.error('ocorreu um erro ao logar', e)

        return func(bot, update, *args, **kwargs)
    return wrapped

def log_update(update):
    username = update.message.from_user.username
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    timestamp = update.message.date.astimezone(timezone)
    text = update.message.text
    chat_type = update.message.chat.type
    chat_id = update.message.chat_id
    group_title = update.message.chat.title
    get_log_collection().insert_one({'timestamp': timestamp, 'first_name': first_name, 'username': username, 'user_id': user_id,
                                        'chat_type': chat_type, 'title': group_title, 'text': text, 'chat_id': chat_id})

def debug(message):
    logging.debug(message)

def info(message):
    logging.info(message)

def warning(message):
    logging.warning(message)

def error(message, ex=None):
    if ex is None:
        logging.error(message)
    else:
        logging.error(message, ex)
