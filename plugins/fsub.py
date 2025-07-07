from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
from client import bot
from utils.helpers import get_group
from search import recent_requests

# ➕ Check if FSub is enabled for group
async def is_fsub_enabled(chat_id):
    group = await get_group(chat_id)
    return group and group.get("f_sub")

# ✅ Check if user is subscribed
async def is_subscribed(bot, message):
    group = await get_group(message.chat.id)
    if not group:
        return True

    fsub = group.get("f_sub")
    if not fsub or not message.from_user:
        return True

    try:
        member = await bot.get_chat_member(fsub, message.from_user.id)
        return member.status in ("member", "administrator", "creator")
    except:
        pass

    try:
        invite_link = (await bot.get_chat(fsub)).invite_link
    except:
        invite_link = f"https://t.me/{fsub.lstrip('@')}"

    await message.reply_text(
        f"🔐 Hello {message.from_user.mention}, to use this bot you must join our channel first!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Channel", url=invite_link)],
            [InlineKeyboardButton("🔄 Try Again", callback_data=f"checksub_{message.from_user.id}")]
        ])
    )
    return False

# 🔁 Retry handler
@bot.on_callback_query(filters.regex("checksub_(\\d+)"))
async def retry_after_join(client, query):
    user_id = int(query.matches[0].group(1))
    if user_id != query.from_user.id:
        return await query.answer("⚠️ This button is not for you!", show_alert=True)

    if user_id in recent_requests:
        await recent_requests[user_id].continue_search()
        await query.message.delete()
        del recent_requests[user_id]
    else:
        await query.answer("⏳ No pending search request found.", show_alert=True)
