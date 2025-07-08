import asyncio
import threading
from flask import Flask
from client import bot
from utils.uptime import notify_if_recent_restart, daily_uptime_report
from pyrogram import idle

# 🌐 Flask App Setup (Render health check)
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot is running!"

# 🚀 Start Flask in a separate thread
def run_flask():
    app.run(host="0.0.0.0", port=10000)

# 🤖 Start Bot
async def start_bot():
    print("🔁 Starting Bot...")

    await bot.start()
    print("✅ Bot Started Successfully!")

    # 🔔 Notify on restart
    await notify_if_recent_restart(bot)

    # 📊 Schedule daily uptime report
    await daily_uptime_report(bot)

    # 🔒 Keep the bot running
    await idle()

    print("🛑 Bot Stopped")


if __name__ == "__main__":
    # 🧵 Start Flask server thread
    threading.Thread(target=run_flask).start()

    # 🌀 Start the bot
    asyncio.run(start_bot())
