import os
import random

from discord.ext import commands
from dotenv import load_dotenv
from dbwork import makedb, filldb, randomquote, removelast, addquote, settingsdb, addsetting, removesetting, checksetting, \
    setprefix, setdefaults, getprefix
from wordlists import getreaction, worddicts, help
from discord.utils import get
from timework import toUTC

import os
import psycopg2

load_dotenv()
STAGE = os.getenv('STAGE')
TOKEN = os.getenv('TOKEN')
ADMIN_ROLE = os.getenv('ADMIN_ROLE')
if STAGE == 'dev':
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

else:
    PSQL_HOST = os.getenv('PSQL_HOST')
    PSQL_USER = os.getenv('PSQL_USER')
    PSQL_DATABASE = os.getenv('PSQL_DATABASE')
    PSQL_PASSWORD = os.getenv('PSQL_PASSWORD')
    conn = psycopg2.connect(
        host=PSQL_HOST,
        user=PSQL_USER,
        dbname=PSQL_DATABASE,
        password=PSQL_PASSWORD
    )





settingsdb(conn)
makedb(conn)
setdefaults(conn)
filldb(conn)
help_items = worddicts()

bot = commands.Bot(command_prefix=(getprefix(conn)))


@bot.command(name='quote', help="generates random quotes with translation", pass_context=True)
async def cookin(ctx):
    chan = ctx.message.channel.id
    if checksetting(conn, 'bot', chan):
        response = randomquote(conn)
        await ctx.send(response)
    await ctx.message.delete()


@bot.command(name='add', help='Adds a quote. Use quotes around both quote and translation', pass_context=True)
async def itl(ctx, language, line, trans=""):
    await ctx.message.delete()
    addquote(conn, language, line, trans)


@bot.command(name='del', help='deletes last quote', pass_context=True)
async def de(ctx):
    await ctx.message.delete()
    removelast(conn)


@bot.command(name='addfunction', help='sets the channel for function', pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def addfunction(ctx, function):
    chan = ctx.channel.id
    print(chan)
    addsetting(conn,function,str(chan))
    await ctx.message.delete()


@bot.command(name='delfunction', help='removes the channel from the function list', pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def delfunction(ctx, function):
    chan = ctx.channel.id
    print(chan)
    removesetting(conn,function,str(chan))
    await ctx.message.delete()


@bot.command(name='invite',help='prints koai invite',pass_context=True)
async def invite(ctx):
    message = "Want to invite a friend? Use this link: \n https://discord.gg/Fuvabsm"
    await ctx.message.delete()
    await ctx.send(message)


@bot.command(name='raid',help='prints link to raid room',pass_context=True)
async def raid(ctx):
    chan = ctx.message.channel.id
    if checksetting(conn, 'accountability', chan):
        message = "RAID IS BEGINNING: \n https://cuckoo.team/koai"
        await ctx.send(message)
    await ctx.message.delete()


@bot.command(name="utc",help="yyyy-mm-dd hh:mm timezone - converts to UTC", pass_context=True)
async def utc(ctx, date, time, zone):
    message = toUTC(date, time, zone)
    await ctx.message.delete()
    await ctx.send(message)


@bot.command(name='info',help='gives info on essential KOAI concepts',pass_context=True)
async def raid(ctx, theme = ""):
    message = help(help_items, theme)
    await ctx.message.delete()
    await ctx.send(message)


@bot.command(name='setpref', help='sets a new prefix for bot',pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def setpref(ctx, prefix):
    setprefix(conn,prefix)
    getprefix(conn)
    x = getprefix(conn)
    bot.command_prefix = x
    await ctx.message.delete()
    message = "Prefix is set to "+x
    await ctx.send(message)


@bot.event
async def on_raw_reaction_add(payload):
    chan = payload.channel_id
    print(checksetting(conn,'accountability', chan))
    if checksetting(conn,'accountability', chan) and payload.emoji.name == "📌":
        msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        await msg.pin()


@bot.event
async def on_raw_reaction_remove(payload):
    chan = payload.channel_id
    if checksetting(conn,'accountability', chan) and payload.emoji.name == "📌":
        print("emoji_removed")
        msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        await msg.unpin()


@bot.event
async def on_message(message):
    chan = message.channel.id
    line = message.content
    print(getreaction(conn,line,chan))
    emo = getreaction(conn,line,chan)
    for i in emo:
        print(i)
        if i[:1] == ':':
            em = i[1:-1]
            emoji = get(bot.emojis, name=em)
            if emoji:
                await message.add_reaction(emoji)
        else:
            await message.add_reaction(i)
    await bot.process_commands(message)









bot.run(TOKEN)
