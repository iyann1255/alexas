from pyrogram.types import Message
from functools import wraps

def paid_subscriber_required(func):
    @wraps(func)
    async def wrapper(_, message: Message):
        user_id = message.from_user.id
        # Misal: cek di database atau API apakah user berlangganan
        if is_paid_subscriber(user_id):
            return await func(_, message)
        else:
            await message.reply("Fitur ini hanya untuk pengguna berlangganan.")
    return wrapper

# Contoh penggunaan:
@paid_subscriber_required
async def your_handler(_, message: Message):
    await message.reply("Selamat datang pengguna premium!")
