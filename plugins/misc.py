from utils import script
from utils import *
from client import bot
from plugins.generate import database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

print("✅ misc.py loaded")


@bot.on_message(filters.command("start") & ~filters.channel)
async def start(bot, message):
    database.insert_one({"chat_id": message.from_user.id})
    username = (await bot.get_me()).username
    await add_user(message.from_user.id, message.from_user.first_name)
    button = [[
        InlineKeyboardButton('➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕', url=f'http://t.me/{username}?startgroup=true')
    ],[
        InlineKeyboardButton("ʜᴇʟᴘ", callback_data="misc_help"),
        InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="misc_about")
    ],[
        InlineKeyboardButton("🤖 ᴜᴘᴅᴀᴛᴇ", url="https://t.me/rmcbackup"),
        InlineKeyboardButton("🔍 ɢʀᴏᴜᴘ", url="https://t.me/rmcmovierequest")
    ]]
    await message.reply(
        text=script.START.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(button)
    )

@bot.on_message(filters.command("help"))
async def help(bot, message):
    await message.reply(
        text=script.HELP,
        disable_web_page_preview=True
    )

@bot.on_message(filters.command("about"))
async def about(bot, message):
    await message.reply(
        text=script.ABOUT.format((await bot.get_me()).mention),
        disable_web_page_preview=True
    )

@bot.on_message(filters.command("stats"))
async def stats(bot, message):
    g_count, _ = await get_groups()
    u_count, _ = await get_users()
    await message.reply(script.STATS.format(u_count, g_count))

@bot.on_message(filters.command("id"))
async def id(bot, message):
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

@bot.on_callback_query(filters.regex(r"^misc"))
async def misc(bot, update):
    data = update.data.split("_")[-1]
    username = (await bot.get_me()).username
    if data == "home":
        button = [[
            InlineKeyboardButton('➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕', url=f'http://t.me/{username}?startgroup=true')
        ],[
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="misc_help"),
            InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="misc_about")
        ],[
            InlineKeyboardButton("🤖 ᴜᴘᴅᴀᴛᴇ", url="https://t.me/rmcbackup"),
            InlineKeyboardButton("🔍 ɢʀᴏᴜᴘ", url="https://t.me/rmcmovierequest")
        ]]
        await update.message.edit(
            text=script.START.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(button)
        )
    elif data == "help":
        await update.message.edit(
            text=script.HELP,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="misc_home")]])
        )
    elif data == "about":
        await update.message.edit(
            text=script.ABOUT.format((await bot.get_me()).mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="misc_home")]])
        )
