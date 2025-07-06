from pyrogram import filters
from pyrogram.types import Message
from client import bot
from config import ADMIN, DATABASE_URI
from pymongo import MongoClient
from pyrogram.errors import PeerIdInvalid, UserIsBlocked, InputUserDeactivated, FloodWait
import asyncio

mongo = MongoClient(DATABASE_URI)
user_collection = mongo.userdb.users

# ✅ Broadcast command
@bot.on_message(filters.command("broadcast") & filters.user(ADMIN))
async def broadcast(_, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply("📌 Reply to a message or use `/broadcast your message here`")

    if message.reply_to_message:
        content = message.reply_to_message
    else:
        content = message.text.split(" ", 1)[1]

    sent, failed = 0, 0
    users = user_collection.find()

    await message.reply("📡 Broadcast started...")

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
            continue

        await asyncio.sleep(0.1)

    await message.reply_text(
        f"✅ Broadcast completed!\n\n"
        f"📤 Sent: {sent}\n❌ Failed: {failed}"
    )
  
