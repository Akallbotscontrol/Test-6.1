# plugins/fsub_utils.py

from config import FORCE_SUB_CHANNEL
from pyrogram.errors import UserNotParticipant

# 🔘 Check if Force Sub is enabled
async def is_fsub_enabled(chat_id):
    from utils.helpers import get_group
    group = await get_group(chat_id)
    return group and group.get("f_sub")

# ✅ Check if user is subscribed
async def is_subscribed(bot, message):
    from utils.helpers import get_group
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
