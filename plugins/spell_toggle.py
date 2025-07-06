from pyrogram import filters
from pyrogram.types import Message
from client import bot
from config import ADMIN
from utils.script import set_spell1, set_spell2, get_spell1, get_spell2

@bot.on_message(filters.command("spell1") & filters.user(ADMIN))
async def toggle_spell1(_, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply_text("🔠 Use `/spell1 on` or `/spell1 off`")
    
    arg = msg.command[1].lower()
    if arg == "on":
        set_spell1(True)
        await msg.reply_text("✅ Spell Checker 1 (fuzzywuzzy) is ON.")
    elif arg == "off":
        set_spell1(False)
        await msg.reply_text("❌ Spell Checker 1 (fuzzywuzzy) is OFF.")
    else:
        await msg.reply_text("⚠️ Invalid option. Use `on` or `off`.")

@bot.on_message(filters.command("spell2") & filters.user(ADMIN))
async def toggle_spell2(_, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply_text("🔠 Use `/spell2 on` or `/spell2 off`")
    
    arg = msg.command[1].lower()
    if arg == "on":
        set_spell2(True)
        await msg.reply_text("✅ Spell Checker 2 (pyspellchecker) is ON.")
    elif arg == "off":
        set_spell2(False)
        await msg.reply_text("❌ Spell Checker 2 (pyspellchecker) is OFF.")
    else:
        await msg.reply_text("⚠️ Invalid option. Use `on` or `off`.")
      
