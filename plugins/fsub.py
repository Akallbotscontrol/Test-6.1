from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from client import bot
from config import ADMIN
from utils.helpers import is_subscribed, recent_requests
from utils.script import set_fsub_status, get_fsub_channel, is_fsub_enabled, set_fsub_channel

# ✅ Admin command: set force subscribe channel
@bot.on_message(filters.command("fsub") & filters.user(ADMIN))
async def set_force_sub_channel(_, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply_text("❌ Usage:\n`/fsub <channel username or ID>`")

    channel = msg.command[1]

    # Try to fetch channel info to validate
    try:
        chat = await bot.get_chat(channel)
        if not chat.id:
            raise Exception("Invalid Chat")
        await set_fsub_channel(chat.id)
        await set_fsub_status(True)
        await msg.reply_text(f"✅ Force Subscribe is now enabled for:\n{chat.title} (`{chat.id}`)")
    except Exception as e:
        await msg.reply_text(f"❌ Failed to set FSUB channel:\n`{e}`")

# ❌ Admin command: disable force subscribe
@bot.on_message(filters.command("nofsub") & filters.user(ADMIN))
async def disable_fsub(_, msg: Message):
    await set_fsub_status(False)
    await msg.reply_text("❌ Force Subscribe is now DISABLED.")

# 🔄 User clicks "✅ I Joined" button
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
