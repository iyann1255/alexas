from asyncio import sleep
from pyrogram import filters
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from pyrogram.enums import MessagesFilter
from pyrogram.raw.functions.messages import DeleteHistory
from aiofiles.os import remove as aremove



@cilik.on_message(filters.command(["dl", "download"]))
async def _(client, message):
    link = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        link = message.reply_to_message.text or message.reply_to_message.caption
    if not link:
        await message.reply("<b>Usage:</b>\n<code>/dl or /download</code> [link]")
    else:
        Tm = await message.reply("<code>Downloading...</code>")
        if "tiktok" in link:
            bot = "downloader_tiktok_bot"
            await ub.one.unblock_user(bot)
            xnxx = await ub.one.send_message(bot, link)
            await xnxx.delete()
            await sleep(3)
            mediafile = []
            async for sosmed in ub.one.search_messages(
                bot, filter=MessagesFilter.PHOTO_VIDEO
            ):
                    

                sfiles = await ub.one.download_media(sosmed)
                if sosmed.video:
                    files = InputMediaVideo(sfiles)
                else:
                    files = InputMediaPhoto(sfiles)


                mediafile.append(files)  
                    
            await client.send_media_group(message.chat.id, mediafile)
            await Tm.delete()
            await aremove(sfiles)
            user_info = await ub.one.resolve_peer(bot)
            return await ub.one.invoke(
                DeleteHistory(peer=user_info, max_id=0, revoke=True)
            )

        elif "instagram" in link:
            bot = "SaveAsBot"
            await ub.one.unblock_user(bot)
            xnxx = await ub.one.send_message(bot, link)
            await xnxx.delete()
            await sleep(5)
            mediafile = []
            async for sosmed in ub.one.search_messages(
                bot, filter=MessagesFilter.PHOTO_VIDEO
            ):
                    

                sfiles = await ub.one.download_media(sosmed)
                if sosmed.video:
                    files = InputMediaVideo(sfiles)
                else:
                    files = InputMediaPhoto(sfiles)


                mediafile.append(files)  
                    
            await client.send_media_group(message.chat.id, mediafile)
            await Tm.delete()
            await aremove(sfiles)                
            user_info = await ub.one.resolve_peer(bot)
            return await ub.one.invoke(
                DeleteHistory(peer=user_info, max_id=0, revoke=True)
            )

        elif "twitter" or "x.com" in link:
            bot = "xvideosdwbot"
            await ub.one.join_chat("xcombotnews")
            await ub.one.unblock_user(bot)
            xnxx = await ub.one.send_message(bot, link)
            await xnxx.delete()
            await sleep(5)
            mediafile = []
            async for sosmed in ub.one.search_messages(
                bot, filter=MessagesFilter.PHOTO_VIDEO
            ):
                    

                sfiles = await ub.one.download_media(sosmed)
                if sosmed.video:
                    files = InputMediaVideo(sfiles)
                else:
                    files = InputMediaPhoto(sfiles)


                mediafile.append(files)  
                    
            await client.send_media_group(message.chat.id, mediafile)
            await Tm.delete()
            await aremove(sfiles)                
            user_info = await ub.one.resolve_peer(bot)
            return await ub.one.invoke(
                DeleteHistory(peer=user_info, max_id=0, revoke=True)
            )                        

        else:
            await message.reply("not valid link")
