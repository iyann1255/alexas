# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""

import asyncio
from AlexaMusic import app
from pyrogram import Client, filters
from datetime import datetime, timedelta
from pyrogram.errors import FloodWait, UserNotParticipant, ChatAdminRequired
from AlexaMusic.core.mongo import db as alexa
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AlexaMusic.utils.database import get_served_users, get_served_chats

OWNER_ID = 7931457261

# Tambahkan ini
FORCE_CHANNEL = "AWDfilm"  # Ganti dengan channel kamu, contoh: "SepMusiqChannel"

# ===============================
# Force Subscribe Decorator
# ===============================
def force_subscribe(func):
    async def wrapper(client, message):
        try:
            user = await client.get_chat_member(FORCE_CHANNEL, message.from_user.id)
            if user.status in ("kicked", "banned"):
                await message.reply_text("🚫 Kamu diblokir dari channel. Hubungi admin.")
                return
        except UserNotParticipant:
            try:
                invite_link = await client.export_chat_invite_link(FORCE_CHANNEL)
            except ChatAdminRequired:
                invite_link = f"https://t.me/{FORCE_CHANNEL}"
            await message.reply_text(
                "🚨 Untuk menggunakan bot ini, kamu harus join dulu ke channel.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("✅ Gabung Sekarang", url=invite_link)]]
                )
            )
            return
        except Exception as e:
            print(f"[ForceSubscribeError] {e}")
            pass  # fallback lanjut
        await func(client, message)  # lanjut kalau sudah join
    return wrapper

# ===============================
# Contoh Handler Pakai Decorator
# ===============================
@app.on_message(filters.private)
@force_subscribe
async def handle_private(client, message):
    await message.reply_text("Halo! Kamu sudah join channel, silakan lanjut pakai bot.")
