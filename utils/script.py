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

# 🔁 Force Subscribe Toggle
def get_fsub_status() -> bool:
    data = toggle_db.find_one({"_id": "fsub"})
    return data["status"] if data else True  # default ON

def set_fsub_status(status: bool):
    toggle_db.update_one({"_id": "fsub"}, {"$set": {"status": status}}, upsert=True)
  
