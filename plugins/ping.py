from pyrogram import filters
from client import bot

@bot.on_message(filters.command("ping"))
async def ping(client, message):
    await message.reply_text("🏓 Pong! I am alive.")
