from pymongo import MongoClient
from config import DATABASE_URI
from utils.helpers import get_group, update_group

# DB setup
mongo = MongoClient(DATABASE_URI)
toggle_db = mongo.userdb.toggles

# 🔁 Spell 1 Toggle (global)
def get_spell1() -> bool:
    data = toggle_db.find_one({"_id": "spell1"})
    return data["status"] if data else True  # default ON

def set_spell1(status: bool):
    toggle_db.update_one({"_id": "spell1"}, {"$set": {"status": status}}, upsert=True)

# 🔁 Spell 2 Toggle (global)
def get_spell2() -> bool:
    data = toggle_db.find_one({"_id": "spell2"})
    return data["status"] if data else True  # default ON

def set_spell2(status: bool):
    toggle_db.update_one({"_id": "spell2"}, {"$set": {"status": status}}, upsert=True)

# 🔁 Force Subscribe Toggle (per-group)
async def get_fsub_status(group_id: int) -> bool:
    group = await get_group(group_id)
    return group.get("f_sub", False) if group else False

async def set_fsub_status(group_id: int, status: bool):
    await update_group(group_id, {"f_sub": status})
