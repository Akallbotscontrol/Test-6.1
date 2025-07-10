import asyncio
import threading
from flask import Flask
from client import bot
from plugins import *  # ✅ Load all plugin handlers
from pyrogram import idle

app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Bot is running!"

# ✅ Run Flask in parallel thread
def run_flask():
    print("✅ Flask server started")
    app.run(host="0.0.0.0", port=10000)

# ✅ Bot runner
async def run_bot():
    await bot.start()
    print("✅ Bot started")
    await idle()

if __name__ == "__main__":
    # Start Flask
    threading.Thread(target=run_flask).start()

    # Start Bot loop
    asyncio.run(run_bot())
