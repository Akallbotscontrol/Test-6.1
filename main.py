import asyncio
import threading
from flask import Flask
from client import bot
from utils.uptime import daily_uptime_report

# ✅ Manually import all plugin modules to ensure handlers are registered
from plugins.misc import *
from plugins.search import *
from plugins.admin import *
from plugins.inline import *
from plugins.connect import *
from plugins.corrector import *
from plugins.fsub import *
from plugins.generate import *
from plugins.newgroup import *
from plugins.help import *
from plugins.speed import *
from plugins.spell_toggle import *
from plugins.spell_toggle_cmd import *
from plugins.verify import *

# 🌐 Flask Web Server
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

    # 🕛 Daily uptime log
    asyncio.create_task(daily_uptime_report(bot))

    # 🌐 Run Flask in background thread
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
