from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from client import bot
from utils import script
from utils.helpers import get_users, get_groups, add_user
from plugins.generate import database

print("✅ misc.py loaded")

# 🔁 Echo Test for private chats excluding command handlers
@bot.on_message(filters.private & ~filters.command(["start", "help", "about", "stats", "id"]))
async def echo_test(client, message):
    print(f"📩 Message received from {message.from_user.id}: {message.text}")
    await message.reply("✅ Bot is receiving messages.")

# 🟢 /start command
@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    print("✅ /start received")
    try:
        database.insert_one({"chat_id": message.from_user.id})
    except:
        pass

    username = (await client.get_me()).username
    await add_user(message.from_user.id, message.from_user.first_name)

    buttons = [
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{username}?startgroup=true")],
        [InlineKeyboardButton("ʜᴇʟᴘ", callback_data="misc_help"), InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="misc_about")],
        [InlineKeyboardButton("🤖 ᴜᴘᴅᴀᴛᴇ", url="https://t.me/rmcbackup"), InlineKeyboardButton("🔍 ɢʀᴏᴜᴘ", url="https://t.me/rmcmovierequest")]
    ]

    await message.reply(
        text=script.START.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ℹ️ /help
@bot.on_message(filters.command("help") & filters.private)
async def help_handler(client, message):
    await message.reply(script.HELP, disable_web_page_preview=True)

# 🧾 /about
@bot.on_message(filters.command("about") & filters.private)
async def about_handler(client, message):
    await message.reply(script.ABOUT.format((await client.get_me()).mention), disable_web_page_preview=True)

# 📊 /stats
@bot.on_message(filters.command("stats") & filters.private)
async def stats_handler(client, message):
    g_count, _ = await get_groups()
    u_count, _ = await get_users()
    await message.reply(script.STATS.format(u_count, g_count))

# 🆔 /id
@bot.on_message(filters.command("id") & filters.private)
async def id_handler(client, message):
    text = f"Current Chat ID: `{message.chat.id}`\n"
    if message.from_user:
        text += f"Your ID: `{message.from_user.id}`\n"
    if message.reply_to_message:
        if message.reply_to_message.from_user:
            text += f"Replied User ID: `{message.reply_to_message.from_user.id}`\n"
        if message.reply_to_message.forward_from:
            text += f"Forwarded From User ID: `{message.reply_to_message.forward_from.id}`\n"
        if message.reply_to_message.forward_from_chat:
            text += f"Forwarded From Chat ID: `{message.reply_to_message.forward_from_chat.id}`\n"
    await message.reply(text)

# 🧷 Callback Buttons
@bot.on_callback_query(filters.regex(r"^misc"))
async def misc_callback_handler(client, update):
    data = update.data.split("_")[-1]
    username = (await client.get_me()).username

    if data == "home":
        buttons = [
            [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{username}?startgroup=true")],
            [InlineKeyboardButton("ʜᴇʟᴘ", callback_data="misc_help"), InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="misc_about")],
            [InlineKeyboardButton("🤖 ᴜᴘᴅᴀᴛᴇ", url="https://t.me/rmcbackup"), InlineKeyboardButton("🔍 ɢʀᴏᴜᴘ", url="https://t.me/rmcmovierequest")]
        ]
        await update.message.edit_text(
            text=script.START.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "help":
        await update.message.edit_text(
            text=script.HELP,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="misc_home")]
            ])
        )

    elif data == "about":
        await update.message.edit_text(
            text=script.ABOUT.format((await client.get_me()).mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="misc_home")]
            ])
        )
