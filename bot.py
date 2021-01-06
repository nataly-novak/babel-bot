import os
import random

from discord.ext import commands
from dotenv import load_dotenv
from dbwork import makedb, filldb, randomquote, removelast, addquote, settingsdb, addsetting, removesetting

import os
import psycopg2

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

settingsdb(conn)

makedb(conn)

filldb(conn)

TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='/')

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


@bot.command(name='delpin', help='rmoves the channel for from pin command list', pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def setpin(ctx):
    chan = ctx.channel.id
    print(chan)
    removesetting(conn,'settingspins',str(chan))


@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "📌":
        msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        await msg.pin()
        ctx = await bot.get_context(msg)
        await ctx.send("Message pinned")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.emoji.name == "📌":
        print("emoji_removed")
        msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        await msg.unpin()
        ctx = await bot.get_context(msg)
        await ctx.send("Message unpinned")



bot.run(TOKEN)
