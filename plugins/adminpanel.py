from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from client import bot
from config import ADMIN
from utils.helpers import get_group_count, get_user_count
from utils.script import get_spell1, get_spell2, set_spell1, set_spell2, get_fsub_status, set_fsub_status

# 📊 Admin Panel Command
@bot.on_message(filters.command("adminpanel") & filters.group & filters.user(ADMIN))
async def admin_panel(_, message: Message):
    group_id = message.chat.id

    # ✅ Fetch current statuses
    fsub = "ON ✅" if await get_fsub_status(group_id) else "OFF ❌"
    spell1 = "ON ✅" if get_spell1() else "OFF ❌"
    spell2 = "ON ✅" if get_spell2() else "OFF ❌"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🔁 Force Subscribe: {fsub}", callback_data=f"toggle_fsub_{group_id}")],
        [InlineKeyboardButton(f"🧠 Spell 1: {spell1}", callback_data="toggle_spell1"),
         InlineKeyboardButton(f"🧠 Spell 2: {spell2}", callback_data="toggle_spell2")],
        [InlineKeyboardButton("📊 User Count", callback_data="user_count"),
         InlineKeyboardButton("👥 Group Count", callback_data="group_count")],
        [InlineKeyboardButton("📡 Broadcast", callback_data="start_broadcast")],
    ])

    await message.reply_text("⚙️ Admin Control Panel", reply_markup=keyboard)

# 🔘 Handle Toggles
@bot.on_callback_query(filters.regex(r"^toggle_"))
async def toggle_handler(_, query: CallbackQuery):
    if query.from_user.id != ADMIN:
        return await query.answer("Access Denied", show_alert=True)

    action = query.data

    if action.startswith("toggle_fsub_"):
        group_id = int(action.split("_")[2])
        current = await get_fsub_status(group_id)
        await set_fsub_status(group_id, not current)
        await query.answer(f"Force Subscribe {'Enabled' if not current else 'Disabled'} ✅", show_alert=True)

    elif action == "toggle_spell1":
        current = get_spell1()
        set_spell1(not current)
        await query.answer(f"Spell 1 {'Enabled' if not current else 'Disabled'} ✅", show_alert=True)

    elif action == "toggle_spell2":
        current = get_spell2()
        set_spell2(not current)
        await query.answer(f"Spell 2 {'Enabled' if not current else 'Disabled'} ✅", show_alert=True)

    # 🔄 Refresh Panel
    await admin_panel(_, query.message)

# 📊 Show User Count
@bot.on_callback_query(filters.regex("user_count"))
async def show_user_count(_, query: CallbackQuery):
    count = await get_user_count()
    await query.answer(f"Total Users: {count}", show_alert=True)

# 👥 Show Group Count
@bot.on_callback_query(filters.regex("group_count"))
async def show_group_count(_, query: CallbackQuery):
    count = await get_group_count()
    await query.answer(f"Total Verified Groups: {count}", show_alert=True)

# 📡 Broadcast Prompt
@bot.on_callback_query(filters.regex("start_broadcast"))
async def start_broadcast(_, query: CallbackQuery):
    await query.answer("Use /broadcast <message> to start", show_alert=True)
