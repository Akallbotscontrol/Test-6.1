from pyrogram import filters
from pyrogram.types import Message
from client import bot
from motor.motor_asyncio import AsyncIOMotorClient
from config import DATABASE_URI

# MongoDB Async setup
mongo = AsyncIOMotorClient(DATABASE_URI)
mode_collection = mongo.userdb.modes

# 🔄 Toggle Mode
@bot.on_message(filters.command("mode") & filters.private)
async def mode_toggle(_, message: Message):
    user_id = message.from_user.id
    user_data = await mode_collection.find_one({"_id": user_id})

    current_mode = user_data["mode"] if user_data else "both"

    if current_mode == "both":
        new_mode = "inline"
    elif current_mode == "inline":
        new_mode = "text"
    else:
        new_mode = "both"

    await mode_collection.update_one(
        {"_id": user_id},
        {"$set": {"mode": new_mode}},
        upsert=True
    )

    await message.reply_text(f"🔁 Your search mode is now set to: **{new_mode.upper()}**")

# 🔍 Get user mode anywhere
async def get_user_mode(user_id: int) -> str:
    user_data = await mode_collection.find_one({"_id": user_id})
    return user_data["mode"] if user_data else "both"
