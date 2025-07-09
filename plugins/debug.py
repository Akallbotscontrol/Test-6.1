from pyrogram import filters
from pyrogram.types import Message
from client import bot

@bot.on_message(filters.all)
async def log_all(bot, message: Message):
    msg_preview = message.text or message.caption or "[Non-text message]"
    print(f"[📩 RECEIVED] Chat ID: {message.chat.id} | From: {message.from_user.id if message.from_user else 'N/A'}\n→ {msg_preview}")
