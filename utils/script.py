from pymongo import MongoClient
from config import DATABASE_URI

mongo = MongoClient(DATABASE_URI)
userdb = mongo.userdb
toggle_db = userdb.toggles
conn_col = userdb.connections  # ✅ Collection for /connect system

# 🔁 Spell 1 Toggle
def get_spell1() -> bool:
    data = toggle_db.find_one({"_id": "spell1"})
    return data["status"] if data else True

def set_spell1(status: bool):
    toggle_db.update_one({"_id": "spell1"}, {"$set": {"status": status}}, upsert=True)

# 🔁 Spell 2 Toggle
def get_spell2() -> bool:
    data = toggle_db.find_one({"_id": "spell2"})
    return data["status"] if data else True

def set_spell2(status: bool):
    toggle_db.update_one({"_id": "spell2"}, {"$set": {"status": status}}, upsert=True)

# 🔁 Force Subscribe Toggle
def get_fsub_status() -> bool:
    data = toggle_db.find_one({"_id": "fsub"})
    return data["status"] if data else True

def set_fsub_status(status: bool):
    toggle_db.update_one({"_id": "fsub"}, {"$set": {"status": status}}, upsert=True)

# 🔌 Add Channel Connection
def add_connection(user_id: int, group_id: int):
    conn_col.update_one(
        {"_id": user_id},
        {"$addToSet": {"group_ids": group_id}},
        upsert=True
    )

# 🔌 Remove Channel Connection
def remove_connection(user_id: int, group_id: int):
    conn_col.update_one(
        {"_id": user_id},
        {"$pull": {"group_ids": group_id}}
    )

# 📋 List All Connections
def list_connections(user_id: int):
    data = conn_col.find_one({"_id": user_id})
    return data.get("group_ids", []) if data else []
