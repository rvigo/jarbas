import os
import sys
import random

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, '../vendored'))

from telegram import Bot, Update, Message


MESSAGES = (
    'Parabéns, {}!',
    '{}, felicidades! ',
    '{}, te desejo tudo de bom!',
    'Sucesso, {}!'
)


def birthday(bot, update, args):
    if args:
        username = args[0]
        bdaymessage = random.choice(MESSAGES)
        bot.send_message(chat_id=update.message.chat_id,
                         text=(bdaymessage.format(username)))
    else:
        update.effective_message.reply_text(
            'Você precisa me dizer quem está fazendo aniversário')
