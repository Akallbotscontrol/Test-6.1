from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import script
from utils.helpers import add_user, get_users, get_groups
from plugins.generate import database

@Client.on_message(filters.command("start") & ~filters.channel)
async def start(bot, message):
    user = message.from_user
    if user:
        database.insert_one({"chat_id": user.id})
        await add_user(user.id, user.first_name)

        username = (await bot.get_me()).username
        buttons = [
            [InlineKeyboardButton("➕ Add Me To Your Group ➕", url=f"https://t.me/{username}?startgroup=true")],
            [InlineKeyboardButton("📖 Help", callback_data="misc_help"),
             InlineKeyboardButton("ℹ️ About", callback_data="misc_about")],
            [InlineKeyboardButton("📢 Updates", url="https://t.me/rmcbackup"),
             InlineKeyboardButton("💬 Group", url="https://t.me/rmcmovierequest")]
        ]
        await message.reply(
            text=script.START.format(user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

@Client.on_message(filters.command("help"))
async def help(bot, message):
    await message.reply(
        text=script.HELP,
        disable_web_page_preview=True
    )

@Client.on_message(filters.command("about"))
async def about(bot, message):
    bot_name = (await bot.get_me()).mention
    await message.reply(
        text=script.ABOUT.format(bot_name),
        disable_web_page_preview=True
    )

@Client.on_message(filters.command("stats"))
async def stats(bot, message):
    g_count, _ = await get_groups()
    u_count, _ = await get_users()
    await message.reply(script.STATS.format(u_count, g_count))

@Client.on_message(filters.command("id"))
async def id(bot, message):
    text = f"Current Chat ID: `{message.chat.id}`\n"
    if message.from_user:
        text += f"Your ID: `{message.from_user.id}`\n"
    if message.reply_to_message:
        reply = message.reply_to_message
        if reply.from_user:
            text += f"Replied User ID: `{reply.from_user.id}`\n"
        if reply.forward_from:
            text += f"Forwarded User ID: `{reply.forward_from.id}`\n"
        if reply.forward_from_chat:
            text += f"Forwarded Chat ID: `{reply.forward_from_chat.id}`\n"
    await message.reply(text)

@Client.on_callback_query(filters.regex(r"^misc"))
async def misc_callback(bot, cb):
    user = cb.from_user
    data = cb.data.split("_")[-1]

    if data == "home":
        username = (await bot.get_me()).username
        buttons = [
            [InlineKeyboardButton("➕ Add Me To Your Group ➕", url=f"https://t.me/{username}?startgroup=true")],
            [InlineKeyboardButton("📖 Help", callback_data="misc_help"),
             InlineKeyboardButton("ℹ️ About", callback_data="misc_about")],
            [InlineKeyboardButton("📢 Updates", url="https://t.me/rmcbackup"),
             InlineKeyboardButton("💬 Group", url="https://t.me/rmcmovierequest")]
        ]
        await cb.message.edit(
            text=script.START.format(user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "help":
        await cb.message.edit(
            text=script.HELP,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="misc_home")]])
        )

    elif data == "about":
        bot_name = (await bot.get_me()).mention
        await cb.message.edit(
            text=script.ABOUT.format(bot_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="misc_home")]])
        )
