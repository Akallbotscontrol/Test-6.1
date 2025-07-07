from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from client import bot
from config import ADMIN
from utils.helpers import is_subscribed, recent_requests
from utils.script import set_fsub_status, get_fsub_status

# ✅ Admin command: enable force subscribe (group-specific)
@bot.on_message(filters.command("fsub") & filters.group & filters.user(ADMIN))
async def enable_fsub(_, msg: Message):
    await set_fsub_status(msg.chat.id, True)
    await msg.reply_text("✅ Force Subscribe is now ENABLED for this group.")

# ❌ Admin command: disable force subscribe (group-specific)
@bot.on_message(filters.command("nofsub") & filters.group & filters.user(ADMIN))
async def disable_fsub(_, msg: Message):
    await set_fsub_status(msg.chat.id, False)
    await msg.reply_text("❌ Force Subscribe is now DISABLED for this group.")

# 🔄 "✅ I Joined" button clicked by user
@bot.on_callback_query(filters.regex("force_check"))
async def fsub_recheck(_, query: CallbackQuery):
    user = query.from_user
    if await is_subscribed(user.id):
        req = recent_requests.get(user.id)
        if req:
            del recent_requests[user.id]
            await query.message.edit("✅ Verified. Please wait...")

            # ⏳ Show "Searching for..." before actual result
            await bot.send_message(
                chat_id=user.id,
                text=f"🔍 Searching for: `{req.query}`..."
            )

            await req.continue_search()
        else:
            await query.message.edit("✅ You have joined. Try again.")
    else:
        await query.answer("❌ You must join the updates channel first!", show_alert=True)
