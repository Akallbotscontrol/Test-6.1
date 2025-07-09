from pyrogram import Client, filters

@Client.on_message(filters.all)
async def log_all(bot, message):
    print(f"[📩 RECEIVED] From {message.chat.id}: {message.text}")
  
