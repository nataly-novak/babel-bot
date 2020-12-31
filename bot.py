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


@bot.command(name='quote', help = "generates random quotes with translation", pass_context=True)
async def cookin(ctx):
    response = randomquote(conn)
    await ctx.send(response)
    await bot.delete_message(ctx.message)



@bot.command(name='add' , help='Adds a quote. Use quotes around both quote and translation', pass_context=True)
async def itl(ctx,language, line, trans =""):
    addquote(conn,language,line,trans)
    await bot.delete_message(ctx.message)

@bot.command(name='del' , help='deletes last quote', pass_context=True)
async def de(ctx):
    removelast(conn)
    await bot.delete_message(ctx.message)

bot.run(TOKEN)