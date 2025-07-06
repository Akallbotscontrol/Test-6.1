from pyrogram import filters
from pyrogram.types import Message
from client import bot
from utils.script import add_connection, remove_connection, list_connections
from config import ADMIN

@bot.on_message(filters.command("connect"))
async def connect_channel(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.forward_from_chat:
        return await message.reply_text("❗ Reply to a forwarded post from the channel you want to connect.")
    
    channel = message.reply_to_message.forward_from_chat
    add_connection(message.from_user.id, channel.id)
    await message.reply_text(f"✅ Connected to `{channel.title}` successfully.")

@bot.on_message(filters.command("disconnect"))
async def disconnect_channel(_, message: Message):
    removed = remove_connection(message.from_user.id)
    if removed:
        await message.reply_text("❎ Disconnected your active connection.")
    else:
        await message.reply_text("⚠️ No active channel found to disconnect.")

@bot.on_message(filters.command("connections"))
async def show_connections(_, message: Message):
    connections = list_connections(message.from_user.id)
    if not connections:
        return await message.reply_text("🔌 No connected channels.")
    
    text = "**🔗 Connected Channels:**\n\n"
    for cid in connections:
        text += f"• `{cid}`\n"
    
    await message.reply_text(text)
  
