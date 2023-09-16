from logging import Logger

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from ...config.models import MessagesConfig

from ..utils import dummy_true, all_content_types


# Unhandled updates

# 1. message - send an unknown_update message
# 2. callback query - send an unknown_update message


async def unhandled_messages_handler(
        message: Message,
        bot: AsyncTeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(
        f"User {message.from_user.id} @{message.from_user.username} in chat {message.chat.id}"
        f"sent an unhandled message with content_type \"{message.content_type}\""
    )
    await bot.send_message(message.chat.id, messages.unknown_update)


async def unhandled_callback_queries_handler(
        call: CallbackQuery,
        bot: AsyncTeleBot,
        messages: MessagesConfig,
        logger: Logger,
        **kwargs):
    logger.debug(
        f"User {call.from_user.id} @{call.from_user.username} in chat {call.message.chat.id}"
        f"sent an unhandled callback query with callback_data \"{call.data}\""
    )
    await bot.send_message(call.message.chat.id, messages.unknown_update)


def register_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(unhandled_messages_handler, content_types=all_content_types, pass_bot=True)
    bot.register_callback_query_handler(unhandled_callback_queries_handler, func=dummy_true, pass_bot=True)
