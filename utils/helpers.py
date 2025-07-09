import asyncio
from config import DATABASE_URI
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client, enums
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChannelInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo.errors import DuplicateKeyError

from client import bot
from plugins.search import recent_requests

# 📦 MongoDB Setup
dbclient = AsyncIOMotorClient(DATABASE_URI)
db = dbclient["Channel-Filter"]
grp_col = db["GROUPS"]
user_col = db["USERS"]
query_col = db["LAST_QUERY"]

# ➤ Group Functions
async def add_group(group_id, group_name, user_name, user_id, channels, f_sub, verified):
    data = {
        "_id": group_id,
        "name": group_name,
        "user_id": user_id,
        "user_name": user_name,
        "channels": channels,
        "f_sub": f_sub,
        "verified": verified
    }
    try:
        await grp_col.insert_one(data)
    except DuplicateKeyError:
        pass

async def get_group(group_id):
    return await grp_col.find_one({"_id": group_id})

async def update_group(group_id, new_data):
    await grp_col.update_one({"_id": group_id}, {"$set": new_data})

async def delete_group(group_id):
    await grp_col.delete_one({"_id": group_id})

async def get_group_count():
    return await grp_col.count_documents({})

async def get_groups():
    count = await grp_col.count_documents({})
    groups = await grp_col.find({}).to_list(length=count)
    return count, groups

# ➤ User Functions
async def add_user(user_id, name):
    try:
        await user_col.insert_one({"_id": user_id, "name": name})
    except DuplicateKeyError:
        pass

async def delete_user(user_id):
    await user_col.delete_one({"_id": user_id})

async def get_user_count():
    return await user_col.count_documents({})

async def get_users():
    count = await user_col.count_documents({})
    users = await user_col.find({}).to_list(length=count)
    return count, users

# ➤ Last Search Query Save (for Retry feature)
async def save_last_query(user_id, chat_id, query):
    await query_col.update_one(
        {"_id": f"{chat_id}_{user_id}"},
        {"$set": {"query": query}},
        upsert=True
    )

async def get_last_query(user_id, chat_id):
    record = await query_col.find_one({"_id": f"{chat_id}_{user_id}"})
    return record["query"] if record else None

# ✅ Force Subscribe Status Check
async def is_subscribed(bot, message):
    group = await get_group(message.chat.id)
    if not group:
        return True

    fsub_channel = group.get("f_sub")
    if not fsub_channel:
        return True

    try:
        member = await bot.get_chat_member(fsub_channel, message.from_user.id)
        if member.status in [
            enums.ChatMemberStatus.MEMBER,
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER
        ]:
            return True
    except UserNotParticipant:
        return False
    except Exception:
        return False

    return False

# ➤ Force Subscribe Check & UI reply
async def force_sub(bot, message):
    group = await get_group(message.chat.id)
    if not group:
        return True

    fsub_channel = group.get("f_sub")
    admin = group.get("user_id")

    if not fsub_channel or not message.from_user:
        return True

    try:
        invite_link = (await bot.get_chat(fsub_channel)).invite_link
        member = await bot.get_chat_member(fsub_channel, message.from_user.id)

        if member.status in [
            enums.ChatMemberStatus.MEMBER,
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER
        ]:
            return True
    except UserNotParticipant:
        pass
    except Exception as e:
        if admin:
            try:
                await bot.send_message(admin, f"❌ Force Subscribe Error:\n`{e}`")
            except:
                pass
        return False

    try:
        await message.reply_text(
            f"🔐 Hello {message.from_user.mention}, you need to join our channel before using this bot.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url=invite_link)],
                [InlineKeyboardButton("🔄 Try Again", callback_data=f"checksub_{message.from_user.id}")]
            ])
        )
    except:
        pass

    return False
