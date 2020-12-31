import os
import random

from discord.ext import commands
from dotenv import load_dotenv
from dbwork import makedb, filldb, randomquote, removelast, addquote

import os
import psycopg2

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

makedb(conn)

filldb(conn)

TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='/')


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


@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "📌":
        await payload.message.pin()
        ctx = await bot.get_context(payload)
        await ctx.send("Message pinned")


bot.run(TOKEN)
