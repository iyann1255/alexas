# AlexaMusic/handlers/start_command.py

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup
from AlexaMusic import app
from AlexaMusic.utils.force_subscribe import force_subscribe
from AlexaMusic.utils.inline import start_pannel  # kamu sudah punya ini
from config import BOT_USERNAME


@app.on_message(filters.command("start") & filters.private)
@force_subscribe
async def start_command(client, message: Message):
    _ = {
        "S_B_1": "ℹ️ Bantuan",
        "S_B_2": "⚙️ Pengaturan",
        "S_B_3": "💬 Grup Diskusi",
        "S_B_4": "📢 Channel",
        "S_B_5": "➕ Tambahkan ke Grup",
        "S_B_6": "📁 Source Code",
        "S_B_7": "👤 Pemilik Bot",
        "S_B_8": "⬅️ Kembali",
    }
    buttons = start_pannel(_)
    await message.reply_text(
        f"Halo {message.from_user.mention}, selamat datang di bot musik!",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
