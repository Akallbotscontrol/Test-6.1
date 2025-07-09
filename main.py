import asyncio
from flask import Flask
from threading import Thread
from client import bot
from utils.uptime import notify_if_recent_restart, daily_uptime_report
from pyrogram.idle import idle

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

async def start_all():
    print("🔁 Starting Bot...")

    await bot.start()
    print("✅ Bot Started Successfully!")

    await notify_if_recent_restart(bot)
    asyncio.create_task(daily_uptime_report(bot))  # Schedule uptime check

    await idle()
    print("🛑 Bot Stopped")

if __name__ == "__main__":
    # Start Flask in a separate thread
    Thread(target=run_flask).start()

    # Start the bot in the main thread loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_all())
