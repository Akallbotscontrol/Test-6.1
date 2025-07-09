from pyrogram import filters
from pyrogram.types import Message
from client import bot
from config import ADMIN
from utils.helpers import get_user_count, get_group_count, get_users
from pyrogram.errors import FloodWait, RPCError
import asyncio

# 👤 Total User Count
@bot.on_message(filters.command("userc") & filters.user(ADMIN))
async def user_count_handler(_, message: Message):
    total = await get_user_count()
    await message.reply_text(f"👤 Total Users: `{total}`")

# 👥 Total Group Count
@bot.on_message(filters.command("groupc") & filters.user(ADMIN))
async def group_count_handler(_, message: Message):
    total = await get_group_count()
    await message.reply_text(f"👥 Total Groups: `{total}`")

# 🛠️ Admin Panel Command List
@bot.on_message(filters.command("adminpanel") & filters.user(ADMIN))
async def admin_panel(_, message: Message):
    await message.reply_text(
        "**🛠️ Admin Panel**\n\n"
        "• `/userc` - Total users\n"
        "• `/groupc` - Total groups\n"
        "• `/mode` - Switch search mode\n"
        "• `/fsub` / `/nofsub` - Toggle Force Subscribe\n"
        "• `/broadcast` - Send message to all users\n",
        quote=True
    )

# 📢 Broadcast Message
@bot.on_message(filters.command("broadcast") & filters.user(ADMIN))
async def broadcast_handler(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("📢 Usage: `/broadcast Your message here`", quote=True)

    broadcast_text = message.text.split(None, 1)[1]
    users_sent = 0
    users_failed = 0

    count, users = await get_users()
    status = await message.reply(f"🔄 Broadcasting to {count} users...")

    for user in users:
        try:
            await bot.send_message(user["_id"], broadcast_text)
            users_sent += 1
            await asyncio.sleep(0.1)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except RPCError as err:
            users_failed += 1
            print(f"[❌] Failed to send to {user['_id']}: {err}")

    await status.edit(
        f"✅ **Broadcast complete!**\n\n"
        f"👤 Total Users: {count}\n"
        f"📬 Sent: {users_sent}\n"
        f"❌ Failed: {users_failed}"
    )
