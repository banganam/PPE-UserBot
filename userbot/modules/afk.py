# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

from random import choice, randint
from asyncio import sleep

from telethon.events import StopPropagation

from userbot import (AFKREASON, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN)
from userbot.events import register

# ========================= CONSTANTS ============================
AFKSTR = [
    "`Sorry, my Boss is offline because is Busy.`",
]
# =================================================================


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    global ISAFK
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if ISAFK:
            if mention.sender_id not in USERS:
                if AFKREASON:
                    await mention.reply(f"`Sorry, my Boss is offline because is {AFKREASON}`")
                else:
                    await mention.reply(str(choice(AFKSTR)))
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                if USERS[mention.sender_id] % 3 == 0:
                    if AFKREASON:
                        await mention.reply("`Hello, i'm a bot!`\n\n"
                       f"`Currently my Boss is still offline because {AFKREASON}`\n\n"
                        "`Please wait until my Boss responds to your message.` 😉👍")
                    else:
                        await mention.reply(str(choice(AFKSTR)))
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True)
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global USERS
    global COUNT_MSG
    if sender.is_private and sender.sender_id != 777000 and not (
            await sender.get_sender()).bot:
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and ISAFK:
            if sender.sender_id not in USERS:
                if AFKREASON:
                    await sender.reply(f"`Sorry, my Boss is offline because is {AFKREASON}`")
                else:
                    await sender.reply(str(choice(AFKSTR)))
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % 3 == 0:
                    if AFKREASON:
                        await sender.reply("`Hello, i'm a bot!`\n\n"
                       f"`Currently my Boss is still offline because {AFKREASON}`\n\n"
                        "`Please wait until my Boss responds to your message.` 😉👍")
                    else:
                        await sender.reply(str(choice(AFKSTR)))
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern="^.afk(?: |$)(.*)")
async def set_afk(afk_e):
    """ For .afk command, allows you to inform people that you are afk when they message you """
    message = afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    if string:
        AFKREASON = string
        await afk_e.edit(f"`You are offline, because {string}`")
    else:
        await afk_e.edit("You are offline now!")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nYou are offline now!")
    ISAFK = True
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    if ISAFK:
        ISAFK = False
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "You recieved " + str(COUNT_MSG) + " messages from " +
                str(len(USERS)) + " when you are offline.",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                    " `Sending` " + "`" + str(USERS[i]) + " message`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None


CMD_HELP.update({
    "afk":
    ".afk [Optional Reason]\
\nUsage: Sets you as afk.\nReplies to anyone who tags/PM's \
you telling them that you are AFK(reason).\n\nSwitches off AFK when you type back anything, anywhere.\
"
})
