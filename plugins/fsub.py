# plugins/fsub.py

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from client import bot
from plugins.fsub_utils import is_fsub_enabled, is_subscribed  # ✅ imported from new file
from plugins.search import recent_requests  # ✅ safe to keep

# 🔁 Retry handler for FSub
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
