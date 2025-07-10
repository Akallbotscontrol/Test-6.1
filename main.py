import asyncio
import threading
from flask import Flask
from client import bot
from plugins import *  # ✅ Auto loads all plugins

app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Bot is running!"

# 🧵 Run Flask in a separate thread
def run_flask():
    app.run(host="0.0.0.0", port=10000)

# 🚀 Start Everything
async def start_all():
    threading.Thread(target=run_flask).start()
    print("✅ Flask server started")
    await bot.start()
    print("✅ Bot started")
    await idle()

if __name__ == "__main__":
    asyncio.run(start_all())
