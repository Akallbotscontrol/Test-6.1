from pyrogram import filters
from pyrogram.types import Message
from client import bot
from utils.script import add_connection, remove_connection, list_connections
from config import ADMIN

# 🔗 Connect a channel via forwarded message (Admin Only)
@bot.on_message(filters.command("connect") & filters.user(ADMIN))
async def connect_channel(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.forward_from_chat:
        return await message.reply_text("❗ Reply to a forwarded post from the channel you want to connect.")
    
    channel = message.reply_to_message.forward_from_chat
    add_connection(message.from_user.id, channel.id)
    await message.reply_text(f"✅ Connected to `{channel.title}` successfully.")

# ❌ Disconnect all connected channels (Admin Only)
@bot.on_message(filters.command("disconnect") & filters.user(ADMIN))
async def disconnect_channel(_, message: Message):
    connections = list_connections(message.from_user.id)
    if not connections:
        return await message.reply_text("⚠️ No connected channels to disconnect.")

    for cid in connections:
        remove_connection(message.from_user.id, cid)
    
    await message.reply_text("❎ Disconnected all connected channels.")

# 📋 Show all connected channels (Admin Only)
@bot.on_message(filters.command("connections") & filters.user(ADMIN))
async def show_connections(_, message: Message):
    connections = list_connections(message.from_user.id)
    if not connections:
        return await message.reply_text("🔌 No connected channels.")
    
    text = "**🔗 Connected Channels:**\n\n"
    for cid in connections:
        text += f"• `{cid}`\n"
    
    await message.reply_text(text)
