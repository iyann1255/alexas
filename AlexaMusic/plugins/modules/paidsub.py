import asyncio
from AlexaMusic import app
from pyrogram import Client, filters
from datetime import datetime, timedelta
from pyrogram.errors import FloodWait
from AlexaMusic.core.mongo import db as alexa
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AlexaMusic.utils.database import get_served_users, get_served_chats


def subcribe(func):
    async def wrapper(_, message: Message):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        if not JOIN:  # Not compulsory
            return
        try:
            try:
                await app.get_chat_member(JOIN, message.from_user.id)
            except UserNotParticipant:
                if JOIN.isalpha():
                    link = "https://t.me/" + JOIN
                else:
                    chat_info = await app.get_chat(JOIN)
                    chat_info.invite_link
                try:
                    await message.reply(
                        f"ʜᴇʏ {rpk}. ᴀɢᴀʀ ʙɪsᴀ ᴍᴇᴍᴜᴛᴀʀ ᴍᴜsɪᴋ, ᴀɴᴅᴀ ʜᴀʀᴜs ᴊᴏɪɴ ᴋᴇ ɢʀᴜᴘ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ . ᴋᴀʟᴀᴜ ᴀᴅᴀ ᴍᴀꜱᴀʟᴀʜ ᴘᴄ @kiritonibos",
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("🗣️ GABUNG SINI 😅", url=link)]]
                        ),
                    )
                    await message.stop_propagation()
                except ChatWriteForbidden:
                    pass
        except ChatAdminRequired:
            await message.reply(
                f"Saya bukan admin di chat : {JOIN} !"
            )
        return await func(_, message)

    return wrapper
