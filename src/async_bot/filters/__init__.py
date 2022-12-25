from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import StateFilter

from storages.async_storages import Storage

from async_bot.logger import Logger
from async_bot.config import Config


def add_custom_filters(bot: AsyncTeleBot, cfg: Config, storage: Storage, logger: Logger):
    bot.add_custom_filter(StateFilter(bot))


__all__ = (
    "add_custom_filters",
)
