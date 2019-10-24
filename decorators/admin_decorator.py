from functools import wraps
from utils import log


def admin(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.message.from_user.id
        if (update.effective_chat.type != 'private' and
                user_id not in get_admin_ids(bot, update.message.chat_id)):

            log.debug(f'not an admin {user_id}.')
            update.effective_message.reply_text(
                'Você precisa ser um admin pra fazer isso')
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
