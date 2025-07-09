from pyrogram import filters
from client import bot
from config import LOG_CHANNEL

@bot.on_message(filters.command("ping"))
async def ping(client, message):
    await message.reply("🏓 Pong!")

@bot.on_message(filters.command("testlog"))
async def test_log_channel(client, message):
    try:
        await client.send_message(LOG_CHANNEL, "🧪 Test message to log channel.")
        await message.reply("✅ Test message sent to log channel.")
    except Exception as e:
        await message.reply(f"❌ Failed to send log: `{e}`")
