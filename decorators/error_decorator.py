from functools import wraps
import sys
import os
import traceback
from utils import log

sys.path.insert(0, './vendored')

from telegram.utils.helpers import mention_html
from telegram import ParseMode


LIST_OF_ADMINS = [os.environ['ADMIN']]


def catch_error(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        try:
            return func(bot, update, *args, **kwargs)
        except Exception as e:
            trace = ''.join(traceback.format_tb(sys.exc_info()[2]))
            payload = ''
            if update.message.from_user:
                payload += f' com o usuario {mention_html(update.message.from_user.id, update.message.from_user.first_name)}'
            if update.message.from_user.username:
                payload += f' (@{update.message.from_user.username})'
            text = f'Hey.\nAconteceu um erro{payload}. Se liga no stacktrace:\n\n<code>{trace}' \
                f'</code>'
            for dev_id in LIST_OF_ADMINS:
                bot.send_message(chat_id=dev_id, text=text,
                                 parse_mode=ParseMode.HTML)
            update.effective_message.reply_text(
                'Alguma coisa deu errado...\nPor favor tente novamente')
            log.error(e)
            raise
    return wrapped
