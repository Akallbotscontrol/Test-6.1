from pyrogram import filters
from pyrogram.types import Message
from client import bot
from config import ADMIN
from utils.script import add_connection, remove_connection, list_connections, get_fsub_channel

# 🔗 /connect command — Connect channel from forwarded post
@bot.on_message(filters.command("connect") & filters.user(ADMIN))
async def connect_channel(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.forward_from_chat:
        return await message.reply_text("❗ Reply to a forwarded post from the channel you want to connect.")
    
    channel = message.reply_to_message.forward_from_chat
    add_connection(message.from_user.id, channel.id)
    await message.reply_text(f"✅ Connected to `{channel.title}` successfully.")

# ❌ /disconnect command — Disconnect all channels
@bot.on_message(filters.command("disconnect") & filters.user(ADMIN))
async def disconnect_channel(_, message: Message):
    connections = list_connections(message.from_user.id)
    if not connections:
        return await message.reply_text("⚠️ No connected channels to disconnect.")

    for cid in connections:
        remove_connection(message.from_user.id, cid)
    
    await message.reply_text("❎ Disconnected all connected channels.")

# 📋 /connections command — Show connected + FSUB channel
@bot.on_message(filters.command("connections") & filters.user(ADMIN))
async def show_connections(_, message: Message):
    connections = list_connections(message.from_user.id)
    fsub_channel = get_fsub_channel()

    text = "**🔗 Connected Channels:**\n\n"
    if connections:
        for cid in connections:
            text += f"• `{cid}`\n"
    else:
        text += "• None\n"

    text += "\n**🔒 Force Subscribe Channel:**\n"
    text += f"• `{fsub_channel}`" if fsub_channel else "• Not Set"

    await message.reply_text(text)
