from config import DATABASE_URI
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, FloodWait
from pymongo.errors import DuplicateKeyError

client = AsyncIOMotorClient(DATABASE_URI)
db = client["Channel-Filter"]
grp_col = db["GROUPS"]
user_col = db["USERS"]
query_col = db["LAST_QUERY"]

# ➤ Group
async def add_group(group_id, group_name, user_name, user_id, channels, f_sub, verified):
    try:
        await grp_col.insert_one({
            "_id": group_id,
            "name": group_name,
            "user_id": user_id,
            "user_name": user_name,
            "channels": channels,
            "f_sub": f_sub,
            "verified": verified
        })
    except DuplicateKeyError:
        pass

async def get_group(id): return await grp_col.find_one({"_id": id})
async def update_group(id, data): await grp_col.update_one({"_id": id}, {"$set": data})
async def delete_group(id): await grp_col.delete_one({"_id": id})
async def get_group_count(): return await grp_col.count_documents({})
async def get_groups(): count = await get_group_count(); return count, await grp_col.find({}).to_list(count)

# ➤ User
async def add_user(id, name):
    try:
        await user_col.insert_one({"_id": id, "name": name})
    except DuplicateKeyError:
        pass

async def delete_user(id): await user_col.delete_one({"_id": id})
async def get_user_count(): return await user_col.count_documents({})
async def get_users(): count = await get_user_count(); return count, await user_col.find({}).to_list(count)

# ➤ Last Query Save
async def save_last_query(user_id, chat_id, query):
    await query_col.update_one({"_id": f"{chat_id}_{user_id}"}, {"$set": {"query": query}}, upsert=True)

async def get_last_query(user_id, chat_id):
    doc = await query_col.find_one({"_id": f"{chat_id}_{user_id}"})
    return doc["query"] if doc else None

# ➤ Force Subscribe
async def force_sub(bot, message):
    group = await get_group(message.chat.id)
    if not group or not group.get("f_sub"): return True

    channel = group.get("f_sub")
    try:
        f_link = (await bot.get_chat(channel)).invite_link
        member = await bot.get_chat_member(channel, message.from_user.id)
        if member.status in [enums.ChatMemberStatus.MEMBER, enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            return True
    except UserNotParticipant:
        pass
    except Exception as e:
        await bot.send_message(group.get("user_id"), f"❌ Force-sub error: `{e}`")
        return False

    await message.reply(
        f"🔐 {message.from_user.mention}, join the channel first!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Channel", url=f_link)],
            [InlineKeyboardButton("🔄 Try Again", callback_data=f"checksub_{message.from_user.id}")]
        ])
    )
    return False
