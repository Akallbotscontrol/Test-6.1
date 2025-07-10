import asyncio
import threading
import logging
from flask import Flask
from client import bot
from plugins import *  # ✅ Load all plugin handlers before bot starts
from pyrogram import idle

# ✅ Logging
logging.basicConfig(level=logging.INFO)

# 🌐 Flask App Setup
app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Bot is running!"

# ✅ Run Flask server in a separate thread
def run_flask():
    print("✅ Flask server started")
    app.run(host="0.0.0.0", port=10000)

# ✅ Start everything
async def start_all():
    # Load handlers first (already done by importing plugins above)
    await bot.start()
    print("✅ Bot started")
    await idle()  # This keeps the bot running

if __name__ == "__main__":
    # Start Flask in parallel
    threading.Thread(target=run_flask).start()

    # Start Bot (async context)
    asyncio.run(start_all())
