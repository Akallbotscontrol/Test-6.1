from pymongo import MongoClient
from config import DATABASE_URI

mongo = MongoClient(DATABASE_URI)
toggle_db = mongo.userdb.toggles
user_collection = mongo.userdb.USERS

START = "👋 Hello {}!\n\nI’m a fast and advanced post search bot. Add me to your group and search from your connected channels."
HELP = "**ℹ️ Help Guide**\n\nUse me to search messages across connected channels.\n\nCommands:\n/start – Welcome\n/id – Get IDs\n/stats – Show stats\n\nAdmins:\n/connect – Link channels\n/fsub – Enable force subscribe\n/verify – Approve bot"
ABOUT = "**🤖 Bot Info**\n\n• Name: {}\n• Language: Python3\n• Framework: Pyrogram\n• Powered by: @RMCBACKUP"
STATS = "**📊 Stats**\n\n👤 Users: `{}`\n👥 Groups: `{}`"

def get_spell1() -> bool:
    data = toggle_db.find_one({"_id": "spell1"})
    return data["status"] if data else True

def set_spell1(status: bool):
    toggle_db.update_one({"_id": "spell1"}, {"$set": {"status": status}}, upsert=True)

def get_spell2() -> bool:
    data = toggle_db.find_one({"_id": "spell2"})
    return data["status"] if data else True

def set_spell2(status: bool):
    toggle_db.update_one({"_id": "spell2"}, {"$set": {"status": status}}, upsert=True)

def get_fsub_status() -> bool:
    data = toggle_db.find_one({"_id": "fsub"})
    return data["status"] if data else True

def set_fsub_status(status: bool):
    toggle_db.update_one({"_id": "fsub"}, {"$set": {"status": status}}, upsert=True)

def get_fsub_channel():
    data = toggle_db.find_one({"_id": "fsub_channel"})
    return data["channel"] if data else None

def set_fsub_channel(channel_username: str):
    toggle_db.update_one({"_id": "fsub_channel"}, {"$set": {"channel": channel_username}}, upsert=True)

def save_user(user_id: int):
    if not user_collection.find_one({"_id": user_id}):
        user_collection.insert_one({"_id": user_id})

def add_connection(user_id: int, channel_id: int):
    record = toggle_db.find_one({"_id": f"conn_{user_id}"})
    channels = record.get("channels", []) if record else []
    if channel_id not in channels:
        channels.append(channel_id)
    toggle_db.update_one({"_id": f"conn_{user_id}"}, {"$set": {"channels": channels}}, upsert=True)

def remove_connection(user_id: int, channel_id: int):
    record = toggle_db.find_one({"_id": f"conn_{user_id}"})
    if record and "channels" in record and channel_id in record["channels"]:
        record["channels"].remove(channel_id)
        toggle_db.update_one({"_id": f"conn_{user_id}"}, {"$set": {"channels": record["channels"]}})
        return True
    return False

def list_connections(user_id: int):
    record = toggle_db.find_one({"_id": f"conn_{user_id}"})
    return record.get("channels", []) if record else []
