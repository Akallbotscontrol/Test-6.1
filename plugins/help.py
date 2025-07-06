from pyrogram import filters
from pyrogram.types import Message
from client import bot
from config import ADMIN

@bot.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    await message.reply_text(
        "👋 Welcome to the Movie Search Bot!\n\n"
        "🔎 Send me any movie name to search.\n"
        "💡 You can also use me in inline mode:\n"
        "`@YourBotName movie name`\n\n"
        "Type /help for full command list.",
        disable_web_page_preview=True
    )

@bot.on_message(filters.command("help"))
async def help_handler(_, message: Message):
    is_admin = message.from_user.id == ADMIN

    text = (
        "📚 **Available Commands**\n\n"
        "**General Commands:**\n"
        "/start - Show welcome message\n"
        "/help - Show this help menu\n"
        "/id - Get your Telegram ID\n"
        "/verify - Login as bot owner\n"
        "/connect - Connect a channel (reply to a forwarded post)\n"
        "/disconnect - Disconnect current connection\n"
        "/connections - List your connected channels\n"
        "/mode - Toggle between inline/text/both search modes\n"
        "/stats - Get total user & group count\n"
        "/userc - Show total user count\n"
        "/groupc - Show total group count with links\n\n"
        "**Spell Checker Controls:**\n"
        "/spell1 on/off - Toggle AI spell checker 1 (fuzzy)\n"
        "/spell2 on/off - Toggle AI spell checker 2 (pyspellchecker)\n\n"
        "**Force Subscribe Controls:**\n"
        "/fsub - Enable force subscription\n"
        "/nofsub - Disable force subscription\n\n"
    )

    if is_admin:
        text += (
            "**🔐 Admin-Only Commands:**\n"
            "/broadcast - Send message to all users\n"
            "/login /logout - Session login system\n"
            "/adminpanel - Show admin controls\n"
        )

    await message.reply_text(text, disable_web_page_preview=True)
  
