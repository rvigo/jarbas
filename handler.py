import json
import os, sys
from services import bus_service, d20_service, react_service, birthday_service, ban_service
from datetime import datetime
from decorators.admin_decorator import admin
from decorators.beta_decorator import beta
from decorators.error_decorator import catch_error
from decorators.restrict_decorator import restricted
from decorators.chat_action_decorator import send_action

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../vendored"))

from telegram.ext import CommandHandler, Dispatcher
from telegram import Bot, Update, Message, User
import telegram
import requests

# sys.path.insert(0, './vendored')


TOKEN = os.environ['TELEGRAM_TOKEN']
send_typing_action = send_action(telegram.ChatAction.TYPING)


@catch_error
@send_typing_action
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Olá {}, eu sou o Jarbas!".format(
        update.message.from_user.first_name))


@catch_error
@send_typing_action
def bus_schedule(bot, update, args):
    telegram_timestamp = update.message.date
    update.effective_message.reply_text(
        bus_service.validate_request(telegram_timestamp, args))


@catch_error
@send_typing_action
def d20(bot, update):
    update.effective_message.reply_text(d20_service.roll_dices())


@catch_error
@restricted
def healthcheck(bot, update):
    update.effective_message.reply_text("200 - ok")


@catch_error
@restricted
@send_typing_action
def react(bot, update):
    react_service.react(bot, update)


@catch_error
@send_typing_action
def birthday(bot, update, args):
    birthday_service.birthday(bot, update, args)


@catch_error
@admin
@send_typing_action
def ban(bot, update, args):
    ban_service.ban(bot, update, args)


def setup(token):
    bot = Bot(token)
    dispatcher = Dispatcher(bot, None, workers=0)

    ##### Register handlers here #####

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('bus', bus_schedule, pass_args=True))
    dispatcher.add_handler(CommandHandler('d20', d20))
    dispatcher.add_handler(CommandHandler('health', healthcheck))
    dispatcher.add_handler(CommandHandler('react', react))
    dispatcher.add_handler(CommandHandler(
        'parabens', birthday, pass_args=True))
    dispatcher.add_handler(CommandHandler('ban', ban, pass_args=True))

    return dispatcher


def webhook(event, context):
    dispatcher = setup(TOKEN)
    try:
        dispatcher.process_update(Update.de_json(
            json.loads(event["body"]), dispatcher.bot))

    except Exception as e:
        print(e)

    return {"statusCode": 200}
