import asyncio
import threading
from flask import Flask
from client import bot
from utils.uptime import notify_if_recent_restart, daily_uptime_report
from pyrogram import idle

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)  # Required for Render

async def start_bot():
    print("🔁 Starting Bot...")

    await bot.start()
    print("✅ Bot Started Successfully!")

    await notify_if_recent_restart(bot)
    asyncio.create_task(daily_uptime_report(bot))  # async scheduler

    await idle()
    print("🛑 Bot Stopped")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(start_bot())
