from pyrogram import filters
from pyrogram.types import Message
from client import bot
from config import ADMIN
from utils.helpers import get_user_count, get_group_count

# 👥 User Count
@bot.on_message(filters.command("userc") & filters.user(ADMIN))
async def user_count_handler(_, message: Message):
    total = await get_user_count()
    await message.reply_text(f"👤 Total Users: `{total}`")

# 👥 Group Count
@bot.on_message(filters.command("groupc") & filters.user(ADMIN))
async def group_count_handler(_, message: Message):
    total = await get_group_count()
    await message.reply_text(f"👥 Total Groups: `{total}`")

# ⚙️ Admin Commands List
@bot.on_message(filters.command("adminpanel") & filters.user(ADMIN))
async def admin_panel(_, message: Message):
    await message.reply_text(
        "**🛠️ Admin Panel**\n\n"
        "• `/userc` - Total users\n"
        "• `/groupc` - Total groups\n"
        "• `/mode` - Switch search mode\n"
        "• `/fsub` / `/nofsub` - Toggle Force Subscribe\n"
        "• `/spell1 on/off` - Toggle Spell Checker 1\n"
        "• `/spell2 on/off` - Toggle Spell Checker 2\n"
        "• `/broadcast` - Send message to all users\n",
        quote=True
    )
