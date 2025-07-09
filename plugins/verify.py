from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from client import bot
from config import LOG_CHANNEL, DATABASE_URI
from pymongo import MongoClient

# ⚙️ MongoDB setup
mongo = MongoClient(DATABASE_URI)
groupdb = mongo.userdb.verified_groups

# 🚨 When bot is added to group
@bot.on_message(filters.new_chat_members)
async def new_group_handler(_, message: Message):
    for member in message.new_chat_members:
        if member.id == (await bot.get_me()).id:
            group_id = message.chat.id
            group_title = message.chat.title

            btn = InlineKeyboardMarkup([[
                InlineKeyboardButton("✅ Verify", callback_data=f"verify_group_{group_id}"),
                InlineKeyboardButton("❌ Unverify", callback_data=f"unverify_group_{group_id}")
            ]])

            await bot.send_message(
                LOG_CHANNEL,
                f"🆕 Bot added to new group:\n\n"
                f"📌 **Group Name:** {group_title}\n"
                f"🆔 **Group ID:** `{group_id}`\n"
                f"👤 Added by: [{message.from_user.first_name}](tg://user?id={message.from_user.id})",
                reply_markup=btn
            )

# ✅ On verify button
@bot.on_callback_query(filters.regex(r"^verify_group_(-?\d+)$"))
async def verify_callback(_, query: CallbackQuery):
    group_id = int(query.matches[0].group(1))

    groupdb.update_one(
        {"group_id": group_id},
        {"$set": {"group_id": group_id, "verified": True}},
        upsert=True
    )

    await query.message.edit_text(f"✅ Group `{group_id}` has been verified.")
    await query.answer("✅ Verified successfully!", show_alert=True)

# ❌ On unverify button
@bot.on_callback_query(filters.regex(r"^unverify_group_(-?\d+)$"))
async def unverify_callback(_, query: CallbackQuery):
    group_id = int(query.matches[0].group(1))

    groupdb.delete_one({"group_id": group_id})

    await query.message.edit_text(f"❌ Group `{group_id}` has been unverified. Bot will no longer respond.")
    await query.answer("❌ Unverified!", show_alert=True)

# 📡 Check if verified (called in search logic or others)
def is_group_verified(group_id: int) -> bool:
    return groupdb.find_one({"group_id": group_id, "verified": True}) is not None
