import asyncio
from client import bot
from pyrogram import idle

async def main():
    await bot.start()
    print("✅ Bot Started")
    await idle()
    print("🛑 Bot Stopped")

if __name__ == "__main__":
    asyncio.run(main())
