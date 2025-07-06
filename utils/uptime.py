import time
import asyncio
from datetime import timedelta, datetime
from config import LOG_CHANNEL

# Bot launch time
START_TIME = time.time()

# 🔁 1. Alert if bot restarts unexpectedly (uptime < 5 min)
async def notify_if_recent_restart(bot):
    uptime = time.time() - START_TIME
    if uptime < 300:
        await bot.send_message(
            LOG_CHANNEL,
            f"🚨 Bot Restart Detected\n⏱️ Current Uptime: {int(uptime)} seconds\n"
            "⚠️ Check if this was expected."
        )

# 📆 2. Daily Uptime Summary at 9:00 AM IST
async def daily_uptime_report(bot):
    while True:
        now = datetime.now()
        if now.hour == 9 and now.minute == 0:
            uptime = str(timedelta(seconds=int(time.time() - START_TIME)))
            await bot.send_message(
                LOG_CHANNEL,
                f"🕒 Daily Uptime Report\nUptime: `{uptime}`"
            )
            await asyncio.sleep(60)  # Avoid duplicate
        await asyncio.sleep(30)
      
