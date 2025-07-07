from pymongo import MongoClient
from config import DATABASE_URI

mongo = MongoClient(DATABASE_URI)
toggle_db = mongo.userdb.toggles

# 🔁 Spell 1
def get_spell1() -> bool:
    data = toggle_db.find_one({"_id": "spell1"})
    return data["status"] if data else True  # default ON

def set_spell1(status: bool):
    toggle_db.update_one({"_id": "spell1"}, {"$set": {"status": status}}, upsert=True)

# 🔁 Spell 2
def get_spell2() -> bool:
    data = toggle_db.find_one({"_id": "spell2"})
    return data["status"] if data else True  # default ON

def set_spell2(status: bool):
    toggle_db.update_one({"_id": "spell2"}, {"$set": {"status": status}}, upsert=True)

# 🔒 Force Subscribe Toggle
def get_fsub_status() -> bool:
    data = toggle_db.find_one({"_id": "fsub"})
    return data["status"] if data else True  # default ON

def set_fsub_status(status: bool):
    toggle_db.update_one({"_id": "fsub"}, {"$set": {"status": status}}, upsert=True)

# 🔒 Get FSUB channel ID
def get_fsub_channel():
    data = toggle_db.find_one({"_id": "fsub_channel"})
    return data["channel"] if data else None

def set_fsub_channel(channel_username: str):
    toggle_db.update_one({"_id": "fsub_channel"}, {"$set": {"channel": channel_username}}, upsert=True)

# 👤 Add connected channel
def add_connection(user_id: int, channel_id: int):
    record = toggle_db.find_one({"_id": f"conn_{user_id}"})
    channels = record.get("channels", []) if record else []
    if channel_id not in channels:
        channels.append(channel_id)
    toggle_db.update_one({"_id": f"conn_{user_id}"}, {"$set": {"channels": channels}}, upsert=True)

# 🔌 Remove connected channel
def remove_connection(user_id: int, channel_id: int):
    record = toggle_db.find_one({"_id": f"conn_{user_id}"})
    if record and "channels" in record and channel_id in record["channels"]:
        record["channels"].remove(channel_id)
        toggle_db.update_one({"_id": f"conn_{user_id}"}, {"$set": {"channels": record["channels"]}})
        return True
    return False

# 🔗 List connected channels
def list_connections(user_id: int):
    record = toggle_db.find_one({"_id": f"conn_{user_id}"})
    return record.get("channels", []) if record else []
