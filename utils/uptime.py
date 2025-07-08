import time
import logging
from datetime import datetime
from config import LOG_CHANNEL
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Track bot start time
start_time = time.time()

# ⏱️ Format uptime into human-readable string
def get_readable_uptime():
    uptime = time.time() - start_time
    days, remainder = divmod(int(uptime), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

# 🔄 Notify when bot restarts
async def notify_if_recent_restart(bot):
    try:
        uptime = get_readable_uptime()
        msg = (
            f"🔄 Bot Restarted\n"
            f"🕒 Uptime: `{uptime}`\n"
            f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        await bot.send_message(LOG_CHANNEL, msg, disable_web_page_preview=True)
        logger.info("✅ Restart notification sent.")
    except Exception as e:
        logger.warning(f"[!] Failed to notify restart: {e}")

# 📊 Send daily uptime report (every day at 12:00 AM)
async def daily_uptime_report(bot):
    async def send_report():
        try:
            uptime = get_readable_uptime()
            msg = (
                f"📊 Daily Uptime Report\n"
                f"🟢 Uptime: `{uptime}`\n"
                f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            await bot.send_message(LOG_CHANNEL, msg, disable_web_page_preview=True)
            logger.info("✅ Daily uptime report sent.")
        except Exception as e:
            logger.warning(f"[!] Failed to send daily report: {e}")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_report, "cron", hour=0, minute=0)  # Every day at midnight
    scheduler.start()
