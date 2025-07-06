from pyrogram import filters
from pyrogram.types import Message
from client import bot
from pymongo import MongoClient
from config import ADMIN, DATABASE_URI
from utils.script import get_spell1, get_spell2, get_fsub_status

mongo = MongoClient(DATABASE_URI)
userdb = mongo.userdb

@bot.on_message(filters.command("stats") & filters.user(ADMIN))
async def bot_stats(_, message: Message):
    total_users = userdb.users.count_documents({})
    total_verified_groups = len(userdb.get_collection("sessions").distinct("chat_id"))

    spell1 = "✅ ON" if get_spell1() else "❌ OFF"
    spell2 = "✅ ON" if get_spell2() else "❌ OFF"
    fsub = "✅ ON" if get_fsub_status() else "❌ OFF"

    await message.reply_text(
        f"📊 **Bot Stats**\n\n"
        f"👤 Total Users: `{total_users}`\n"
        f"👥 Verified Groups: `{total_verified_groups}`\n\n"
        f"🧠 Spell 1: {spell1}\n"
        f"🧠 Spell 2: {spell2}\n"
        f"🔁 Force Subscribe: {fsub}"
    )
  
