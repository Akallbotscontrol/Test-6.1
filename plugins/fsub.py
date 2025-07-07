from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from client import bot
from utils.helpers import get_group, update_group, is_subscribed, recent_requests
from pyrogram.errors import UserNotParticipant

# ✅ /fsub - Set force-subscribe channel for this group
@bot.on_message(filters.command("fsub") & filters.group)
async def set_group_fsub(_, msg: Message):
    if not msg.from_user:
        return

    group_id = msg.chat.id
    user_id = msg.from_user.id

    group = await get_group(group_id)
    if not group or group.get("user_id") != user_id:
        return await msg.reply_text("❌ Only group owner (who verified this group) can set FSUB channel.")

    if len(msg.command) < 2:
        return await msg.reply("❌ Usage:\n`/fsub <channel username or ID>`")

    channel = msg.command[1]

    try:
        chat = await bot.get_chat(channel)
        if not chat.id:
            raise Exception("Invalid Channel")
        await update_group(group_id, {"f_sub": chat.id})
        await msg.reply_text(f"✅ Force Subscribe is now enabled for: {chat.title}")
    except Exception as e:
        await msg.reply_text(f"❌ Failed to set FSUB:\n`{str(e)}`")

# ❌ /nofsub - Disable FSUB for this group
@bot.on_message(filters.command("nofsub") & filters.group)
async def disable_group_fsub(_, msg: Message):
    group_id = msg.chat.id
    user_id = msg.from_user.id

    group = await get_group(group_id)
    if not group or group.get("user_id") != user_id:
        return await msg.reply_text("❌ Only group owner can disable FSUB.")

    await update_group(group_id, {"f_sub": None})
    await msg.reply_text("❌ Force Subscribe has been disabled for this group.")

# 🔄 Force Check (Try Again Button)
@bot.on_callback_query(filters.regex("force_check"))
async def fsub_recheck(_, query: CallbackQuery):
    user = query.from_user
    if await is_subscribed(user.id):
        req = recent_requests.get(user.id)
        if req:
            del recent_requests[user.id]
            await query.message.edit("✅ Verified. Please wait...")

            await bot.send_message(
                chat_id=user.id,
                text=f"🔍 Searching for: `{req.query}`...",
            )
            await req.continue_search()
        else:
            await query.message.edit("✅ You have joined. Try again.")
    else:
        await query.answer("❌ You must join the updates channel first!", show_alert=True)
