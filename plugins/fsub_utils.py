# plugins/fsub_utils.py

from config import FORCE_SUB_CHANNEL
from pyrogram.errors import UserNotParticipant

# 🔘 Check if Force Sub is Enabled
async def is_fsub_enabled() -> bool:
    return bool(FORCE_SUB_CHANNEL)

# ✅ Check if User is Subscribed
async def is_subscribed(bot, user_id: int) -> bool:
    try:
        user = await bot.get_chat_member(FORCE_SUB_CHANNEL, user_id)
        return user.status not in ("kicked", "banned")
    except UserNotParticipant:
        return False
    except Exception:
        return False
      
