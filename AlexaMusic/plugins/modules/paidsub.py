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
from pyrogram.errors import FloodWait
from AlexaMusic.core.mongo import db as alexa
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AlexaMusic.utils.database import get_served_users, get_served_chats

OWNER_ID = 7931457261

# Database collections for subscriptions
SUBSCRIPTION_COLLECTION = "subscriptions"
PAYMENT_COLLECTION = "payments"

# Subscription plans
SUBSCRIPTION_PLANS = {
    "basic": {
        "price": 10000,  # IDR 10,000
        "duration": 30,  # 30 days
        "features": ["Unlimited music requests", "Priority support"]
    },
    "premium": {
        "price": 25000,  # IDR 25,000
        "duration": 30,
        "features": ["All Basic features", "Exclusive commands", "No ads"]
    },
    "vip": {
        "price": 50000,  # IDR 50,000
        "duration": 30,
        "features": ["All Premium features", "24/7 dedicated support", "Custom commands"]
    }
}

async def is_subscribed(user_id: int) -> bool:
    """Check if user has active subscription"""
    subscription = await alexa[SUBSCRIPTION_COLLECTION].find_one(
        {"user_id": user_id, "expiry_date": {"$gt": datetime.now()}}
    )
    return subscription is not None

async def get_subscription_plans_keyboard():
    """Generate inline keyboard for subscription plans"""
    buttons = []
    for plan_name, plan_details in SUBSCRIPTION_PLANS.items():
        buttons.append(
            [
                InlineKeyboardButton(
                    f"{plan_name.capitalize()} - Rp{plan_details['price']:,}",
                    callback_data=f"subscribe_{plan_name}"
                )
            ]
        )
    buttons.append([InlineKeyboardButton("❌ Close", callback_data="close_subscription")])
    return InlineKeyboardMarkup(buttons)

@app.on_message(filters.command("subscribe") & filters.private)
async def subscribe_command(client, message):
    """Handle /subscribe command"""
    if await is_subscribed(message.from_user.id):
        await message.reply("🎉 You already have an active subscription!")
        return
    
    keyboard = await get_subscription_plans_keyboard()
    await message.reply(
        "💎 Choose your subscription plan:\n\n"
        "• Basic: Rp10,000/month\n"
        "• Premium: Rp25,000/month\n"
        "• VIP: Rp50,000/month\n\n"
        "Click the button below to select:",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("^subscribe_"))
async def subscribe_callback(client, callback_query):
    """Handle subscription plan selection"""
    plan_name = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id
    
    if plan_name not in SUBSCRIPTION_PLANS:
        await callback_query.answer("Invalid plan selected!")
        return
    
    plan = SUBSCRIPTION_PLANS[plan_name]
    expiry_date = datetime.now() + timedelta(days=plan["duration"])
    
    # Save subscription
    await alexa[SUBSCRIPTION_COLLECTION].update_one(
        {"user_id": user_id},
        {
            "$set": {
                "plan": plan_name,
                "price": plan["price"],
                "purchase_date": datetime.now(),
                "expiry_date": expiry_date,
                "features": plan["features"]
            }
        },
        upsert=True
    )
    
    # Record payment
    await alexa[PAYMENT_COLLECTION].insert_one({
        "user_id": user_id,
        "amount": plan["price"],
        "plan": plan_name,
        "payment_date": datetime.now(),
        "status": "completed"
    })
    
    await callback_query.message.edit_text(
        f"🎉 Successfully subscribed to {plan_name.capitalize()} plan!\n\n"
        f"• Price: Rp{plan['price']:,}\n"
        f"• Expiry: {expiry_date.strftime('%d %B %Y')}\n\n"
        "Thank you for your support! ❤️"
    )

@app.on_callback_query(filters.regex("^close_subscription$"))
async def close_subscription(client, callback_query):
    """Close subscription menu"""
    await callback_query.message.delete()

@app.on_message(filters.command("mysub") & filters.private)
async def my_subscription(client, message):
    """Check user's subscription status"""
    subscription = await alexa[SUBSCRIPTION_COLLECTION].find_one(
        {"user_id": message.from_user.id}
    )
    
    if not subscription:
        await message.reply("You don't have any active subscription. Use /subscribe to get one!")
        return
    
    expiry_date = subscription["expiry_date"]
    remaining_days = (expiry_date - datetime.now()).days
    
    if remaining_days <= 0:
        status = "❌ Expired"
    else:
        status = f"✅ Active ({remaining_days} days remaining)"
    
    await message.reply(
        f"📝 Your Subscription Details:\n\n"
        f"• Plan: {subscription['plan'].capitalize()}\n"
        f"• Price: Rp{subscription['price']:,}\n"
        f"• Purchased: {subscription['purchase_date'].strftime('%d %B %Y')}\n"
        f"• Expiry: {expiry_date.strftime('%d %B %Y')}\n"
        f"• Status: {status}\n\n"
        f"Features:\n" + "\n".join(f"  - {feature}" for feature in subscription["features"])
    )

# Admin commands
@app.on_message(filters.command("addsub") & filters.user(OWNER_ID))
async def add_subscription(client, message):
    """Add subscription manually (admin only)"""
    if len(message.command) < 4:
        await message.reply("Usage: /addsub [user_id] [plan] [days]")
        return
    
    try:
        user_id = int(message.command[1])
        plan_name = message.command[2].lower()
        days = int(message.command[3])
    except ValueError:
        await message.reply("Invalid parameters!")
        return
    
    if plan_name not in SUBSCRIPTION_PLANS:
        await message.reply("Invalid plan! Available plans: basic, premium, vip")
        return
    
    plan = SUBSCRIPTION_PLANS[plan_name]
    expiry_date = datetime.now() + timedelta(days=days)
    
    await alexa[SUBSCRIPTION_COLLECTION].update_one(
        {"user_id": user_id},
        {
            "$set": {
                "plan": plan_name,
                "price": plan["price"],
                "purchase_date": datetime.now(),
                "expiry_date": expiry_date,
                "features": plan["features"]
            }
        },
        upsert=True
    )
    
    await message.reply(
        f"Successfully added {plan_name} subscription for user {user_id} "
        f"valid until {expiry_date.strftime('%d %B %Y')}"
    )

@app.on_message(filters.command("substats") & filters.user(OWNER_ID))
async def subscription_stats(client, message):
    """Get subscription statistics (admin only)"""
    active_subs = await alexa[SUBSCRIPTION_COLLECTION].count_documents(
        {"expiry_date": {"$gt": datetime.now()}}
    )
    total_subs = await alexa[SUBSCRIPTION_COLLECTION].count_documents({})
    total_revenue = sum(
        payment["amount"] async for payment in alexa[PAYMENT_COLLECTION].find({})
    )
    
    await message.reply(
        "📊 Subscription Statistics:\n\n"
        f"• Active Subscriptions: {active_subs}\n"
        f"• Total Subscriptions: {total_subs}\n"
        f"• Total Revenue: Rp{total_revenue:,}\n\n"
        "Use /subusers to see subscribed users list"
    )

@app.on_message(filters.command("subusers") & filters.user(OWNER_ID))
async def subscribed_users(client, message):
    """List all subscribed users (admin only)"""
    users = []
    async for sub in alexa[SUBSCRIPTION_COLLECTION].find(
        {"expiry_date": {"$gt": datetime.now()}}
    ):
        users.append(
            f"👤 User: {sub['user_id']} | Plan: {sub['plan']} | "
            f"Expires: {sub['expiry_date'].strftime('%d %B %Y')}"
        )
    
    if not users:
        await message.reply("No active subscriptions found.")
        return
    
    text = "📋 Active Subscriptions:\n\n" + "\n".join(users)
    await message.reply(text)

async def check_expired_subscriptions():
    """Periodically check and notify about expired subscriptions"""
    while True:
        expired_subs = alexa[SUBSCRIPTION_COLLECTION].find(
            {"expiry_date": {"$lt": datetime.now()}}
        )
        async for sub in expired_subs:
            try:
                await app.send_message(
                    sub["user_id"],
                    f"⚠️ Your {sub['plan']} subscription has expired!\n\n"
                    "Use /subscribe to renew your subscription and continue enjoying premium features."
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                pass
        
        await asyncio.sleep(3600)  # Check every hour

# Start subscription checker
asyncio.create_task(check_expired_subscriptions())

