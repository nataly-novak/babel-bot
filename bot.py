import os
import random

from discord.ext import commands
from dotenv import load_dotenv
from dbwork import makedb, filldb, randomquote, removelast, addquote, settingsdb, addsetting, removesetting, checksetting, setprefix, setdefaults, getprefix

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

@bot.command(name='setpin', help='sets the channel for pins', pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def setpin(ctx):
    chan = ctx.channel.id
    print(chan)
    addsetting(conn,'settingspins',str(chan))
    await ctx.message.delete()


@bot.command(name='delpin', help='removes the channel for from pin command list', pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def setpin(ctx):
    chan = ctx.channel.id
    print(chan)
    removesetting(conn,'settingspins',str(chan))
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
    x = getprefix(conn)
    await ctx.message.delete()
    message = "Prefix is set to "+x
    await ctx.send(message)





@bot.event
async def on_raw_reaction_add(payload):
    chan = payload.channel_id
    print(checksetting(conn,'settingspins', chan))
    if checksetting(conn,'settingspins', chan) and payload.emoji.name == "📌":
        msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        await msg.pin()



@bot.event
async def on_raw_reaction_remove(payload):
    chan = payload.channel_id
    if checksetting(conn,'settingspins', chan) and payload.emoji.name == "📌":
        print("emoji_removed")
        msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        await msg.unpin()





bot.run(TOKEN)
