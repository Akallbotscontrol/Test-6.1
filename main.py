import asyncio
import threading
from flask import Flask
from client import bot
from utils.uptime import notify_if_recent_restart, daily_uptime_report

app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Bot is running!"

# 🧵 Run Flask in a separate thread
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# 💤 Async Idle Loop for Pyrogram
async def idle():
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Gracefully shutting down...")

# 🚀 Start Everything
async def start_all():
    print("🔁 Starting Bot...")
    await bot.start()
    print("✅ Bot Started Successfully!")

    # 🔄 Notify restart to log channel
    await notify_if_recent_restart(bot)

    # 🕛 Schedule daily uptime
    asyncio.create_task(daily_uptime_report(bot))

    # 🌐 Start Flask app in background thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # ⏳ Keep the bot running
    await idle()

if __name__ == "__main__":
    try:
        asyncio.run(start_all())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Bot stopped manually.")
