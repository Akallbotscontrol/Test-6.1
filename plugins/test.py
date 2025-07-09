from pyrogram import filters
from pyrogram.types import Message
from client import bot

@bot.on_message(filters.private & filters.command("ping"))
async def test_ping(client, message: Message):
    print("✅ /ping command received")
    await message.reply_text("✅ Pong!")
  
