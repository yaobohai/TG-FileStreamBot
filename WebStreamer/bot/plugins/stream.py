# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import logging
import re
import requests
from pyrogram import filters, errors
from WebStreamer.vars import Var
from urllib.parse import quote_plus
from WebStreamer.bot import StreamBot, logger
from WebStreamer.utils import get_hash, get_name
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@StreamBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ),
    group=4,
)

# def replace_context(url):
#     resource_url = url.replace("https://tele-stream-bot.init.ac:443/", "http://tele-stream-bot.private.svc.cluster.local:443/")
#     resource_name = re.search(r'\/([^\/]+)\?', url).group(1)
#     return resource_url, resource_name.split('?')[0]

def download_task(name, url):
    headers = {
        'authority': Var.SAVE_SERVER,
        'cookie': 'connect.sid=s%3AXDax-Pgemsnj4yMvOcBJjb2biCwKTlrt.4ZfR0TCYlwUogvrPlEnxKLdRj91Ws9fzvHTQBR4ABak'
    }

    data = {
        'name': name,
        'URL': url
    }
    response = requests.post(Var.SAVE_SERVER, headers=headers, json=data)

    if response.status_code == 200:
        logger.info(f"提交下载任务成功: {name},状态码: {response.status_code}")
    else:
        logger.info(f"提交下载任务失败: {name},状态码: {response.status_code}")

async def media_receive_handler(_, m: Message):
    if Var.ALLOWED_USERS and not ((str(m.from_user.id) in Var.ALLOWED_USERS) or (m.from_user.username in Var.ALLOWED_USERS)):
        return await m.reply("You are not <b>allowed to use</b> this <a href='https://github.com/EverythingSuckz/TG-FileStreamBot'>bot</a>.", quote=True)
    log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
    file_hash = get_hash(log_msg, Var.HASH_LENGTH)
    stream_link = f"{Var.URL}{log_msg.id}/{quote_plus(get_name(m))}?hash={file_hash}"
    short_link = f"{Var.URL}{file_hash}{log_msg.id}"
    logger.info(f"Generated link: {stream_link} for {m.from_user.first_name}")
    if Var.AUTO_SAVE == 'True':
        print(f"获取的url: {stream_link}")
        # url = replace_context(stream_link)
        # download_task(url[1], url[0])
    try:
        await m.reply_text(
            text="<code>{}</code>\n(<a href='{}'>shortened</a>)".format(
                stream_link, short_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Open", url=stream_link)]]
            ),
        )
    except errors.ButtonUrlInvalid:
        await m.reply_text(
            text="<code>{}</code>\n\nshortened: {})".format(
                stream_link, short_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
        )
