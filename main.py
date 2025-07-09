import asyncio
import threading
from flask import Flask
from client import bot
from utils.uptime import notify_if_recent_restart, daily_uptime_report

app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Idle for Pyrogram v2.x
async def idle():
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass

async def start_all():
    print("🔁 Starting Bot...")
    await bot.start()
    print("✅ Bot Started Successfully!")
    await notify_if_recent_restart(bot)
    asyncio.create_task(daily_uptime_report(bot))
    idle_thread = threading.Thread(target=run_flask)
    idle_thread.start()
    await idle()
    print("🛑 Bot Stopped")

if __name__ == "__main__":
    asyncio.run(start_all())
