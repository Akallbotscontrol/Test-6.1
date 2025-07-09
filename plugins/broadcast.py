from pyrogram import filters
from pyrogram.types import Message
from client import bot
from config import ADMIN, DATABASE_URI
from pymongo import MongoClient
from pyrogram.errors import PeerIdInvalid, UserIsBlocked, InputUserDeactivated, FloodWait
import asyncio

# 🔗 MongoDB
mongo = MongoClient(DATABASE_URI)
user_collection = mongo.userdb.users

# 📡 Broadcast Command (reply or direct)
@bot.on_message(filters.command("broadcast") & filters.user(ADMIN))
async def broadcast(_, message: Message):
    # 📎 Check input
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply("📌 Use `/broadcast your message here` or reply to a message.")

    content = message.reply_to_message if message.reply_to_message else message.text.split(" ", 1)[1]

    sent = 0
    failed = 0
    await message.reply("📡 Broadcast started...")

    users = user_collection.find()

    for user in users:
        user_id = user.get("user_id")
        if not user_id:
            continue

        try:
            if isinstance(content, Message):
                await content.copy(chat_id=user_id)
            else:
                await bot.send_message(user_id, content)
            sent += 1
        except (PeerIdInvalid, UserIsBlocked, InputUserDeactivated):
            failed += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            failed += 1
        await asyncio.sleep(0.1)

    await message.reply_text(
        f"✅ Broadcast completed!\n\n"
        f"📤 Sent: {sent}\n❌ Failed: {failed}"
    )
