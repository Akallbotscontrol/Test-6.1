from pymongo import MongoClient
from config import DATABASE_URI

# 📦 MongoDB Setup
mongo = MongoClient(DATABASE_URI)
db = mongo.userdb
toggle_db = db.toggles
user_collection = db.USERS

# 🔁 Spell 1 Toggle
def get_spell1() -> bool:
    data = toggle_db.find_one({"_id": "spell1"})
    return data["status"] if data and "status" in data else True  # default ON

def set_spell1(status: bool):
    toggle_db.update_one({"_id": "spell1"}, {"$set": {"status": status}}, upsert=True)

# 🔁 Spell 2 Toggle
def get_spell2() -> bool:
    data = toggle_db.find_one({"_id": "spell2"})
    return data["status"] if data and "status" in data else True  # default ON

def set_spell2(status: bool):
    toggle_db.update_one({"_id": "spell2"}, {"$set": {"status": status}}, upsert=True)

# 🔐 Force Subscribe Toggle
def get_fsub_status() -> bool:
    data = toggle_db.find_one({"_id": "fsub"})
    return data["status"] if data and "status" in data else True  # default ON

def set_fsub_status(status: bool):
    toggle_db.update_one({"_id": "fsub"}, {"$set": {"status": status}}, upsert=True)

# 🔐 Get / Set FSUB channel
def get_fsub_channel() -> str | None:
    data = toggle_db.find_one({"_id": "fsub_channel"})
    return data["channel"] if data and "channel" in data else None

def set_fsub_channel(channel_username: str):
    toggle_db.update_one({"_id": "fsub_channel"}, {"$set": {"channel": channel_username}}, upsert=True)

# 👤 Save User in DB
def save_user(user_id: int):
    if not user_collection.find_one({"_id": user_id}):
        user_collection.insert_one({"_id": user_id})

# 🔗 Add Connected Channel
def add_connection(user_id: int, channel_id: int):
    record = toggle_db.find_one({"_id": f"conn_{user_id}"})
    channels = record.get("channels", []) if record else []
    if channel_id not in channels:
        channels.append(channel_id)
        toggle_db.update_one(
            {"_id": f"conn_{user_id}"},
            {"$set": {"channels": channels}},
            upsert=True
        )

# ❌ Remove Connected Channel
def remove_connection(user_id: int, channel_id: int) -> bool:
    record = toggle_db.find_one({"_id": f"conn_{user_id}"})
    if record and "channels" in record:
        channels = record["channels"]
        if channel_id in channels:
            channels.remove(channel_id)
            toggle_db.update_one(
                {"_id": f"conn_{user_id}"},
                {"$set": {"channels": channels}}
            )
            return True
    return False

# 📋 List Connected Channels
def list_connections(user_id: int) -> list:
    record = toggle_db.find_one({"_id": f"conn_{user_id}"})
    return record.get("channels", []) if record else []
