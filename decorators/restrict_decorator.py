from functools import wraps

LIST_OF_ADMINS = [752671006]

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.message.from_user.id
        if user_id not in LIST_OF_ADMINS:
            print(f'Unauthorized access denied for {user_id}.')
            return
        return func(bot, update, *args, **kwargs)
    return wrapped