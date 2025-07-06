import asyncio
from client import bot
# ❌ from plugins.verify import check_unverified_groups  ← Remove this line
from utils.uptime import notify_if_recent_restart, daily_uptime_report
from pyrogram import idle
from flask import Flask
import threading

# ✅ Bot start block
async def start_bot():
    print("🔁 Starting Bot...")

    await bot.start()
    print("✅ Bot Started Successfully!")

    # 🔔 Alert if recently restarted
    await notify_if_recent_restart(bot)

    # 🔍 Skip unverified group check (optional)
    # await check_unverified_groups(bot)

    # 🕒 Start daily uptime task
    asyncio.create_task(daily_uptime_report(bot))

    # 💤 Idle mode
    await idle()

# 🌐 Mini Flask app for uptime ping
app = Flask(__name__)

@app.route('/')
def alive():
    return '✅ Bot is alive - BY RMCBACKUP'

def run_flask():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()  # 🚀 Run Flask
    asyncio.run(start_bot())                     # 🤖 Run Bot
