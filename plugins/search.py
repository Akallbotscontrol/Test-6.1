from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from client import bot
from utils.helpers import (
    get_last_query,
    save_last_query,
    is_user_verified,
    check_force_subscribe,
    search_in_channels
)

# Commands that should NOT trigger search
EXCLUDED_COMMANDS = [
    "start", "help", "about", "stats", "id", "login", "logout",
    "connect", "disconnect", "verify", "connections", "broadcast",
    "adminpannel", "mode", "user", "userc", "groupc", "fsub", "nofsub"
]

@bot.on_message(filters.private & filters.text & ~filters.command(EXCLUDED_COMMANDS))
async def search_handler(client, message):
    user_id = message.from_user.id
    query = message.text.strip()

    if not query:
        return

    # ✅ Force-subscribe check
    if not await check_force_subscribe(client, message):
        await save_last_query(user_id, query)
        return  # User must click Try Again after joining

    # ✅ Optional verify check (if using /verify system)
    if not await is_user_verified(user_id):
        await message.reply("❗ Please verify using /verify command.")
        return

    # 🔍 Save query for retry
    await save_last_query(user_id, query)

    # 🕵️ Show searching feedback
    await message.reply(f"🔎 Searching for: `{query}`", quote=True)

    # 🔍 Search logic
    results = await search_in_channels(query)

    if not results:
        return await message.reply("❌ No results found.", quote=True)

    # ✅ Paginate and send first 5 results
    page = 1
    total_pages = (len(results) + 4) // 5
    await send_paginated_results(message, results, page, total_pages)

# 📤 Pagination Callback Handler
@bot.on_callback_query(filters.regex(r"^page_\d+"))
async def pagination_callback(client, query):
    user_id = query.from_user.id
    data = query.data.split("_")
    page = int(data[1])

    last_query = await get_last_query(user_id)
    if not last_query:
        return await query.answer("❌ No recent search to paginate.", show_alert=True)

    results = await search_in_channels(last_query)
    total_pages = (len(results) + 4) // 5

    await query.message.edit_text("🔄 Loading page...")
    await send_paginated_results(query.message, results, page, total_pages)
    await query.answer()

# 📦 Helper to Send Paginated Results
async def send_paginated_results(message, results, page, total_pages):
    start = (page - 1) * 5
    end = start + 5
    chunk = results[start:end]

    text = f"🔍 **Results (Page {page}/{total_pages}):**\n\n"
    for i, res in enumerate(chunk, start=1):
        text += f"{start + i}. {res}\n"

    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"page_{page - 1}"))
    if page < total_pages:
        buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"page_{page + 1}"))

    markup = InlineKeyboardMarkup([buttons]) if buttons else None
    await message.reply(text, reply_markup=markup, disable_web_page_preview=True)
