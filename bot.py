import os
import random

from discord.ext import commands
from dotenv import load_dotenv
from dbwork import makedb, filldb, randomquote, removelast, addquote, settingsdb, addsetting, removesetting, checksetting, \
    setprefix, setdefaults, getprefix
from wordlists import getreaction
from discord.utils import get

import os
import psycopg2

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

settingsdb(conn)
makedb(conn)
setdefaults(conn)
filldb(conn)

TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix=(getprefix(conn)))

ADMIN_ROLE = os.getenv('ADMIN_ROLE')


@bot.command(name='quote', help="generates random quotes with translation", pass_context=True)
async def cookin(ctx):
    response = randomquote(conn)
    await ctx.message.delete()
    await ctx.send(response)


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
        if em[:1] == ':':
            em = i[1:-1]
            emoji = get(bot.emojis, name=em)
            if emoji:
                await message.add_reaction(emoji)
        else:
            await message.add_reaction(i)
    await bot.process_commands(message)









bot.run(TOKEN)
