from pyrogram import filters
from pyrogram.types import Message
from client import bot
from config import ADMIN
from utils.script import get_spell1, set_spell1, get_spell2, set_spell2

@bot.on_message(filters.command("spell1") & filters.user(ADMIN))
async def toggle_spell1(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/spell1 on` or `/spell1 off`")

    arg = message.command[1].lower()
    if arg == "on":
        set_spell1(True)
        await message.reply_text("✅ SpellChecker 1 is now **ON**")
    elif arg == "off":
        set_spell1(False)
        await message.reply_text("❌ SpellChecker 1 is now **OFF**")
    else:
        await message.reply_text("❌ Invalid. Use `/spell1 on` or `/spell1 off`")

@bot.on_message(filters.command("spell2") & filters.user(ADMIN))
async def toggle_spell2(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/spell2 on` or `/spell2 off`")

    arg = message.command[1].lower()
    if arg == "on":
        set_spell2(True)
        await message.reply_text("✅ SpellChecker 2 is now **ON**")
    elif arg == "off":
        set_spell2(False)
        await message.reply_text("❌ SpellChecker 2 is now **OFF**")
    else:
        await message.reply_text("❌ Invalid. Use `/spell2 on` or `/spell2 off`")
