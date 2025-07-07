from pyrogram import filters
from pyrogram.types import Message
from client import bot
from config import ADMIN
from utils.helpers import update_group, get_group

@bot.on_message(filters.command("fsub") & filters.group)
async def set_group_fsub(_, msg: Message):
    if not msg.from_user:
        return

    group_id = msg.chat.id
    user_id = msg.from_user.id

    group = await get_group(group_id)
    if not group or group.get("user_id") != user_id:
        return await msg.reply_text("❌ Only group owner (verifier) can set FSUB channel.")

    if len(msg.command) < 2:
        return await msg.reply("Usage: /fsub <channel username or ID>")

    channel = msg.command[1]

    try:
        chat = await bot.get_chat(channel)
        if not chat.id:
            raise Exception("Invalid channel")
        await update_group(group_id, {"f_sub": chat.id})
        await msg.reply_text(f"✅ Force Subscribe set to: {chat.title}")
    except Exception as e:
        await msg.reply_text(f"❌ Failed to set FSUB:\n`{str(e)}`")
