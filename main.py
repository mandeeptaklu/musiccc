import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL
from config import Config

app = Client("MusicBot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)
userbot = Client("Assistant", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.SESSION_STRING)

# Music Client
call = PyTgCalls(userbot)

# YouTube Settings
ydl_opts = {"format": "bestaudio/best", "quiet": True}
ydl = YoutubeDL(ydl_opts)

@app.on_message(filters.command("play") & filters.group)
async def play_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("🔎 Gaane ka naam toh likho! Example: `/play Pehle Bhi Main` ")

    query = " ".join(message.command[1:])
    m = await message.reply_text(f"📥 `{query}` ko dhund raha hoon...")

    try:
        # YouTube se link nikalna
        info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        url = info['url']
        title = info['title']
        
        # Voice Chat Join aur Play logic
        await call.join_group_call(
            message.chat.id,
            AudioPiped(url)
        )
        
        await m.edit(f"🎶 **Playing:** [{title}]({info['webpage_url']})", disable_web_page_preview=True)
        
        # Logger group mein update bhejein
        await app.send_message(Config.LOGGER_ID, f"#PLAYING\nChat: `{message.chat.title}`\nSong: {title}")

    except Exception as e:
        await m.edit(f"❌ Error: {e}")
@app.on_message(filters.command("stop") & filters.user(Config.SUDO_USERS))
async def stop_music(client, message):
    try:
        await call.leave_group_call(message.chat.id)
        await message.reply_text("⏹ Music band kar diya gaya hai.")
    except:
        await message.reply_text("❌ Abhi koi gaana nahi chal raha.")

async def start_bot():
    await app.start()
    await userbot.start()
    await call.start()
    print("✅ Music Bot Ready!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_bot())

