import os
import random

from discord.ext import commands
from dotenv import load_dotenv
from dbwork import makedb, filldb

import os
import psycopg2

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')


makedb(conn)

filldb(conn)


TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')