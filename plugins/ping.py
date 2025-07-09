@bot.on_message(filters.command("testlog"))
async def test_log_channel(client, message):
    try:
        await client.send_message(LOG_CHANNEL, "🧪 Test message to log channel.")
        await message.reply("✅ Test message sent to log channel.")
    except Exception as e:
        await message.reply(f"❌ Failed to send log: `{e}`")
