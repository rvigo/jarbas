from functools import wraps

LIST_OF_ADMINS = [os.environ['ADMIN']]

def beta(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user = update.message.from_user.first_name
        if update.message.from_user.id not in LIST_OF_ADMINS:
            update.effective_message.reply_text(f"Desculpe {user}, esta função ainda está em teste...")
            return
        return func(bot, update, *args, **kwargs)
    return wrapped