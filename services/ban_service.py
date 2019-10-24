import os
import sys
import random
from decorators.admin_decorator import get_admin_ids

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, '../vendored'))

from telegram import Message, Chat, Update, Bot, User
from telegram.error import BadRequest
from telegram.ext import run_async, CommandHandler, Filters
from telegram.utils.helpers import mention_html
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, User, CallbackQuery
from telegram import Message, MessageEntity


def ban(bot, update, args):
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    if chat.type == 'private':
        message.reply_text('Esse comando só funciona em grupos.')
        return
    if bot.id not in get_admin_ids(bot, update.message.chat_id):
        message.reply_text('Eu preciso ser um admin para banir alguém aqui...')
        return

    user_id = None
    reason = None

    if (update.message is not None and
        update.message.reply_to_message is not None and
            update.message.reply_to_message.from_user is not None):

        user_id = update.message.reply_to_message.from_user.id

    if len(args) != 0:
        reason = str(' '.join(args))

    if not user_id:
        message.reply_text('Você precisa me dizer quem eu devo banir...')
        return

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == 'User not found':
            message.reply_text('Esse usuário não está no grupo...')
            return
        else:
            raise

    if user_id == bot.id:
        message.reply_text('Eu não posso me banir!')
        return

    reply = '{} partiu dessa para uma melhor.'.format(
        mention_html(member.user.id, member.user.first_name))
    if reason:
        reply += f'\nO motivo? <i>{reason}</i>'

    try:
        chat.kick_member(user_id)

        message.reply_text(reply, parse_mode=ParseMode.HTML)

    except BadRequest as excp:
        if excp.message == 'Reply message not found':

            message.reply_text('', quote=False)
            return
        elif excp.message == 'User is an administrator of the chat':
            message.reply_text('Eu não posso banir outro admin.')
        else:
            print(
                f'ERROR banning user {user_id} in chat {chat.title} ({chat.id}) due to {excp.message}')
            message.reply_text('Não consigo banir esse cara...')

    return
