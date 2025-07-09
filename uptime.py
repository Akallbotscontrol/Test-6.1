import time
from datetime import datetime
from config import LOG_CHANNEL
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 🚀 Track bot start time
start_time = time.time()

# ⏱️ Uptime Formatter
def get_readable_uptime():
    uptime = time.time() - start_time
    days, rem = divmod(int(uptime), 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

# 🔄 Notify on Restart
async def notify_if_recent_restart(bot):
    try:
        await bot.get_chat(LOG_CHANNEL)  # ✅ PeerID resolve
        uptime = get_readable_uptime()
        msg = f"🔄 Bot Restarted\n🕒 Uptime: `{uptime}`\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        await bot.send_message(LOG_CHANNEL, msg)
    except Exception as e:
        print(f"[!] Restart notify failed: {e}")

# 📆 Daily Uptime Report
async def daily_uptime_report(bot):
    async def send_report():
        try:
            await bot.get_chat(LOG_CHANNEL)
            uptime = get_readable_uptime()
            msg = f"📊 Daily Uptime Report\n🟢 Uptime: `{uptime}`\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            await bot.send_message(LOG_CHANNEL, msg)
        except Exception as e:
            print(f"[!] Daily report failed: {e}")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_report, "cron", hour=0, minute=0)  # ⏰ 12:00 AM UTC
    scheduler.start()
