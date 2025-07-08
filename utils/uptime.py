import os
import time
from datetime import datetime
from config import LOG_CHANNEL
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Track start time
start_time = time.time()

# ⏱️ Format uptime
def get_readable_uptime():
    uptime = time.time() - start_time
    days, remainder = divmod(int(uptime), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

# 🔁 Notify restart
async def notify_if_recent_restart(bot):
    try:
        # 👇 Force peer resolve to avoid Peer ID errors
        await bot.get_chat(LOG_CHANNEL)

        uptime = get_readable_uptime()
        msg = f"🔄 Bot Restarted\n🕒 Uptime: `{uptime}`\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        await bot.send_message(LOG_CHANNEL, msg)
    except Exception as e:
        print(f"[!] Failed to notify restart: {e}")

# 📅 Daily uptime report
async def daily_uptime_report(bot):
    async def send_report():
        try:
            await bot.get_chat(LOG_CHANNEL)  # 👈 Ensure peer is resolved
            uptime = get_readable_uptime()
            msg = f"📊 Daily Uptime Report\n🟢 Uptime: `{uptime}`\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            await bot.send_message(LOG_CHANNEL, msg)
        except Exception as e:
            print(f"[!] Failed to send daily report: {e}")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_report, "cron", hour=0, minute=0)  # Daily at 12:00 AM
    scheduler.start()
