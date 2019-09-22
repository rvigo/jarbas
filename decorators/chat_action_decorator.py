from functools import wraps

def send_action(action):
    def decorator(func):
        @wraps(func)
        def wrapped(bot, update, *args, **kwargs):
            bot.send_chat_action(chat_id=update.message.chat_id, action=action)
            return func(bot, update,  *args, **kwargs)
        return wrapped
    return decorator