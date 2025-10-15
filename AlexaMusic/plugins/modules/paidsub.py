import asyncio
from AlexaMusic import app
from pyrogram import Client, filters
from datetime import datetime, timedelta
from pyrogram.errors import FloodWait
from AlexaMusic.core.mongo import db as alexa
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AlexaMusic.utils.database import get_served_users, get_served_chat

MUST_JOIN = "aseppppv"
#------------------------
@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await app.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_photo(
                    photo="https://files.catbox.moe/4j30vg.jpg", caption=f"<blockquote><b>Silahkan bergabung dulu [Support]({link}) ,jika ingin menggunakan bot ini, jika sudah bergabung silahkan ulangi /start</b></blockquote>",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("ðŸŽµ JOIN DULU", url="https://t.me/MaulKak"),
                            ]
                        ]
                    )
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"Promosi saya sebagai admin digrup/channels yang diFSUB: {MUST_JOIN} !")
