from logging import Logger

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from ...config.models import MessagesConfig, ButtonsConfig

from .. import keyboards


# Basic commands

# 1. start - send a welcome message with help reply keyboard
# 2. help - send a help message


async def start_handler(
        message: Message,
        bot: AsyncTeleBot,
        messages: MessagesConfig,
        buttons: ButtonsConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} started the bot")
    await bot.send_message(message.chat.id, messages.welcome, reply_markup=keyboards.help_reply_keyboard(buttons.help))


async def help_handler(
        message: Message,
        bot: AsyncTeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(f"User {message.from_user.id} @{message.from_user.username} requested help")
    await bot.send_message(message.chat.id, messages.help)


def register_handlers(bot: AsyncTeleBot, buttons: ButtonsConfig):
    bot.register_message_handler(start_handler, commands=['start'], pass_bot=True)

    bot.register_message_handler(help_handler, commands=['help'], pass_bot=True)
    bot.register_message_handler(help_handler, text_equals=buttons.help, pass_bot=True)
