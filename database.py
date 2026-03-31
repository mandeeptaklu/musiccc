from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

client = AsyncIOMotorClient(Config.MONGO_URL)
db = client.MusicBotDB
sudo_db = db.sudoers

async def is_sudo(user_id):
    if user_id in Config.SUDO_USERS:
        return True
    return await sudo_db.find_one({"user_id": user_id}) is not None

