from pyrogram import Client, filters
from pyrogram.types import Message
from utils.script import get_spell1, set_spell1, get_spell2, set_spell2

@Client.on_message(filters.command("spell1"))
async def toggle_spell1(_, message: Message):
    current = get_spell1()
    set_spell1(not current)
    status = "enabled ✅" if not current else "disabled ❌"
    await message.reply_text(f"🧠 SpellChecker 1 is now {status}")

@Client.on_message(filters.command("spell2"))
async def toggle_spell2(_, message: Message):
    current = get_spell2()
    set_spell2(not current)
    status = "enabled ✅" if not current else "disabled ❌"
    await message.reply_text(f"🔍 SpellChecker 2 is now {status}")
  
