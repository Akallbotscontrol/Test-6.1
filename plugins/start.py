from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from client import bot
from config import DATABASE_URI, SUPPORT, ADMIN
from pymongo import MongoClient

mongo = MongoClient(DATABASE_URI)
userdb = mongo.userdb

@bot.on_message(filters.command("start") & filters.private)
async def start_command(_, message: Message):
    user = message.from_user
    user_id = user.id

    # ✅ Save user to DB
    userdb.users.update_one(
        {"user_id": user_id},
        {"$set": {
            "user_id": user_id,
            "name": user.first_name,
        }},
        upsert=True
    )

    # ✅ Start message
    text = f"""👋 Hello {user.mention}!
I'm your personal Movie/Series Search Bot 🎬

Search by typing any movie name.
Use buttons below to explore.

🔒 Powered by @RMCBACKUP"""

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 Search Inline", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("📢 Updates", url="https://t.me/RMCBACKUP"),
         InlineKeyboardButton("❓ Help", callback_data="help_menu")],
    ])

    await message.reply(text, reply_markup=buttons)


@bot.on_message(filters.group)
async def group_entry_register(_, message: Message):
    # ✅ Optionally register group (useful for /groupc)
    chat = message.chat
    if chat.id < 0:
        userdb.groups.update_one(
            {"chat_id": chat.id},
            {"$set": {"chat_id": chat.id, "title": chat.title}},
            upsert=True
        )
      
