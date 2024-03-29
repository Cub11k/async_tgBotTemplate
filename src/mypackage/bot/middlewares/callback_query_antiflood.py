import time

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery
from telebot.asyncio_handler_backends import BaseMiddleware, CancelUpdate


class CallbackQueryAntiFloodMiddleware(BaseMiddleware):
    def __init__(self, bot: AsyncTeleBot, timeout_message: str, timeout: float):
        super().__init__()
        self.bot = bot
        self.timeout_message = timeout_message
        self.timeout = timeout
        self.update_types = ['callback_query']
        self.last_query = {}

    # argument naming is kept from the base class to avoid possible errors if passed as kwargs
    async def pre_process(self, message: CallbackQuery, data: dict):
        now = time.time()
        if message.from_user.id not in self.last_query:
            self.last_query[message.from_user.id] = now
            await self.bot.answer_callback_query(message.id)  # always answer callback query
            return
        if now - self.last_query[message.from_user.id] < self.timeout:
            self.last_query[message.from_user.id] = now
            await self.bot.answer_callback_query(message.id, self.timeout_message, show_alert=True)
            return CancelUpdate()
        self.last_query[message.from_user.id] = now
        await self.bot.answer_callback_query(message.id)  # always answer callback query

    # argument naming is kept from the base class to avoid possible errors if passed as kwargs
    async def post_process(self, message: CallbackQuery, data: dict, exception: BaseException):
        pass
