from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from client import bot
from plugins.generate import is_logged_in
from plugins.script import get_spell1, get_spell2, toggle_spell1, toggle_spell2
from plugins.fsub import toggle_fsub, get_fsub_status
from utils.helpers import get_user_count, get_group_count

@bot.on_message(filters.command("adminpanel") & filters.private)
async def admin_panel(_, message: Message):
    if not is_logged_in(message.from_user.id):
        return await message.reply("🚫 You must /login first.")

    panel = InlineKeyboardMarkup([
        [InlineKeyboardButton("📡 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("👤 Users", callback_data="admin_users"),
         InlineKeyboardButton("👥 Groups", callback_data="admin_groups")],
        [InlineKeyboardButton(f"🧠 Spell1: {'ON' if get_spell1() else 'OFF'}", callback_data="admin_toggle_spell1"),
         InlineKeyboardButton(f"🧠 Spell2: {'ON' if get_spell2() else 'OFF'}", callback_data="admin_toggle_spell2")],
        [InlineKeyboardButton(f"🔁 FSub: {'ON' if get_fsub_status() else 'OFF'}", callback_data="admin_toggle_fsub")],
        [InlineKeyboardButton("🚪 Logout", callback_data="admin_logout")]
    ])

    await message.reply("🛠️ **Admin Panel:**", reply_markup=panel)

@bot.on_callback_query(filters.regex(r"^admin_"))
async def admin_callback(_, query: CallbackQuery):
    user_id = query.from_user.id
    if not is_logged_in(user_id):
        return await query.answer("🚫 Not authorized", show_alert=True)

    data = query.data

    if data == "admin_users":
        count = get_user_count()
        return await query.answer(f"👤 Users: {count}", show_alert=True)

    if data == "admin_groups":
        count = get_group_count()
        return await query.answer(f"👥 Groups: {count}", show_alert=True)

    if data == "admin_toggle_spell1":
        toggle_spell1()
        return await query.answer(f"Spell1 toggled!", show_alert=True)

    if data == "admin_toggle_spell2":
        toggle_spell2()
        return await query.answer(f"Spell2 toggled!", show_alert=True)

    if data == "admin_toggle_fsub":
        toggle_fsub()
        return await query.answer("FSub toggled!", show_alert=True)

    if data == "admin_logout":
        from plugins.generate import LOGGED_IN_USERS
        LOGGED_IN_USERS.discard(user_id)
        return await query.answer("Logged out!", show_alert=True)

    if data == "admin_broadcast":
        await query.message.reply("📡 Send the broadcast message now (text only).")

