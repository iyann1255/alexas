# AlexaMusic/utils/force_subscribe.py

from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

FORCE_CHANNEL = "AWDfilm"  # Ganti dengan username channel kamu tanpa '@'

def force_subscribe(func):
    async def wrapper(client, message):
        try:
            user = await client.get_chat_member(FORCE_CHANNEL, message.from_user.id)
            if user.status in ("kicked", "banned"):
                await message.reply_text("🚫 Kamu diblokir dari channel.")
                return
        except UserNotParticipant:
            try:
                invite_link = await client.export_chat_invite_link(FORCE_CHANNEL)
            except ChatAdminRequired:
                invite_link = f"https://t.me/{FORCE_CHANNEL}"
            await message.reply_text(
                "❗ Untuk menggunakan bot ini, kamu harus join dulu ke channel.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("✅ Gabung Channel", url=invite_link)]]
                ),
            )
            return
        except Exception as e:
            print(f"[ForceSubscribeError] {e}")
            pass
        return await func(client, message)
    return wrapper
