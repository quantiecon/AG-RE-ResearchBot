"""
Telegram push logic.
Splits messages longer than Telegram's 4096-char limit automatically.
"""
import logging
import os

from telegram import Bot

logger = logging.getLogger(__name__)

_MAX_LEN = 4096


async def send_message(text: str) -> None:
    bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    for i in range(0, len(text), _MAX_LEN):
        chunk = text[i : i + _MAX_LEN]
        await bot.send_message(chat_id=chat_id, text=chunk)
        logger.info(f"Telegram chunk sent ({len(chunk)} chars)")
