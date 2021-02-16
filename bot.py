import os
import random

from discord.ext import commands, tasks
import discord
from dotenv import load_dotenv
from dbwork import makedb, filldb, randomquote, removelast, addquote, settingsdb, addsetting, removesetting, checksetting, \
    setprefix, setdefaults, getprefix, quotenum
from wordlists import getreaction, worddicts, help
from discord.utils import get
from timework import toUTC, currentUTC, toLocal, getToday, utcToday
from languages import checkrole, roletochan, addlanguage, languagedb, checkchan
from randomer import coin, rannum
from scheduler import maketimetable, addevent, geteventlist, convertlist, remevent
from pombase import makepombases, checkgame, setgame, setuserval,getuserval, setraidstat, getraidstat, getaction
from pommer import Pommer
from stamper import line_update
from mechanics import ranpop
from raid import  Raid

import os
import psycopg2
import pytz
import datetime


intents = discord.Intents.all()

load_dotenv()
STAGE = os.getenv('STAGE')
TOKEN = os.getenv('TOKEN')
ADMIN_ROLE = os.getenv('ADMIN_ROLE')
EVENT = os.getenv('EVENT')
if STAGE == 'dev':
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

elif STAGE == 'local':
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL)

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
cur = conn.cursor()

cur.execute("DROP TABLE pommers, pombase")

settingsdb(conn)
makedb(conn)
setdefaults(conn)
filldb(conn)
help_items = worddicts()
languagedb(conn)
maketimetable(conn)
makepombases(conn)





bot = commands.Bot(command_prefix=(getprefix(conn)),intents=intents)

bot.hug_counter = 0
bot.hug_breaker = 0
bot.minutes = 0
bot.raid_id = 0
bot.account_id = 0
bot.raidlen = 25
bot.on_raid = False
bot.raidbreak = True
bot.raidstatus = 0
bot.raid_members = []
bot.eventchan = 0
bot.common = 0
bot.evrole = []
bot.keepers = 0
bot.isgame = checkgame(conn)
bot.congrats = 0
bot.current_raid = Raid("",0,"")
bot.current_raiders = {}
bot.raider_actions = {}

@bot.event
async def on_ready():
    print ("Booting up your system")
    print ("I am running on " + bot.user.name)
    print ("With the ID: " + str(bot.user.id))
    for guild in bot.guilds:
        for channel in guild.text_channels:
            print(channel.name)
            if checkchan(channel.name):
                print(channel.name)
                addlanguage(conn,channel.name, channel.id)
            elif channel.name == "event-announcements":
                print(channel.id)
                print(channel.name)
                bot.eventchan = channel.id
            elif channel.name == "common-room":
                print(channel.id)
                bot.common = channel.id
            elif channel.name == "keepers-table":
                bot.keepers = channel.id
        for role in guild.roles:
            line = str(role.name)
            print(line)
            if line == "Events":
                print("!!!!!")
                print(role.name)
                bot.evrole.append(role)
        if bot.evrole:
            print(bot.evrole[0].id)

    updater.start()





@bot.command(name='quote', help="generates random quotes with translation", pass_context=True)
async def cookin(ctx):
    chan = ctx.message.channel.id
    if checksetting(conn, 'bot', chan):
        response = randomquote(conn)
        await ctx.send(response)
    await ctx.message.delete()


@bot.command(name='add', help='Adds a quote. Use quotes around both quote and translation', pass_context=True)
async def itl(ctx, language, line, trans=""):
    chan = ctx.message.channel.id
    if checksetting(conn, 'bot', chan):
        message = addquote(conn, language, line, trans)
        await ctx.send(message)


@bot.command(name='del', help='deletes last quote', pass_context=True)
async def de(ctx):
    chan = ctx.message.channel.id
    if checksetting(conn, 'bot', chan):
        await ctx.message.delete()
        message = removelast(conn)
        await ctx.send(message)


@bot.command(name='quotenumber', help='deletes last quote', pass_context=True)
async def quotenumber(ctx):
    chan = ctx.message.channel.id
    if checksetting(conn, 'bot', chan):
        await ctx.message.delete()
        message = quotenum(conn)
        await ctx.send(message)


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
async def invite(ctx, invite = "koai"):
    if invite == "koai":
        message = "Want to invite a friend? Use this link: \n https://discord.gg/Fuvabsm"
    elif invite == "koa":
        message = "Do you want to join Knights of Academia, too? Use this link: \n https://discord.gg/EYX7XGG"
    await ctx.message.delete()
    await ctx.send(message)


@bot.command(name='raid',help='prints link to raid room',pass_context=True)
async def raid(ctx, times = '25'):
    chan = ctx.message.channel.id
    if checksetting(conn, 'accountability', chan):
        if len(bot.raid_members) !=0:
            bot.raid_members = []
            print(bot.current_raid.stamp, bot.current_raid.mmbr)
            for i in bot.current_raiders:
                user = i.user
                print(bot.raider_actions[user])
                setuserval(conn, i)
            setraidstat(conn, bot.current_raid)
            bot.raidstatus = 0
            bot.raider_actions = {}
            bot.current_raiders = {}
        if bot.on_raid == False:
            bot.raidlen = int(times)
            message = "```WAITING FOR RAID OF " +times+  " MINUTES TO START.....```"
            sent = await ctx.send(message)
            bot.account_id = ctx.message.channel.id
            await ctx.message.delete()
            bot.raid_id = sent.id
            await sent.pin()
            bot.on_raid = True
            bot.raidbreak = True
            await sent.add_reaction("🗡")
            await sent.add_reaction("⚔")
            bot.raidstatus = 1
            if getraidstat(conn):
                bot.current_raid = getraidstat(conn)


        else:
            message = "TIMER IS ALREADY ON, SEE PINNED MESSAGES"
            await ctx.send(message)
            await ctx.message.delete()

@bot.command(name='break',help='prints link to raid room',pass_context=True)
async def breaks(ctx, times = '5'):
    chan = ctx.message.channel.id
    if checksetting(conn, 'accountability', chan):
        if bot.on_raid == False:
            bot.raidlen = int(times)
            message = "```WAITING FOR BREAK OF " + times + " MINUTES TO START.....```"
            sent = await ctx.send(message)
            bot.account_id = ctx.message.channel.id
            await ctx.message.delete()
            bot.raid_id = sent.id
            await sent.pin()
            bot.on_raid = True
            bot.raidbreak = False
            await sent.add_reaction("🛏️")
            await sent.add_reaction("💤")
            bot.raidstatus = 1

        else:
            message = "TIMER IS ALREADY ON, SEE PINNED MESSAGES"
            await ctx.send(message)
            await ctx.message.delete()




@bot.command(name="utc",help="yyyy-mm-dd hh:mm timezone:Continent/City - converts to UTC", pass_context=True)
async def utc(ctx, date="", time="", zone=""):
    if date=="" and time=="" and zone == "":
        message = currentUTC()
    elif time != "" and zone != "":
        if date == "today":
            date = getToday(zone)
        message = toUTC(date, time, zone)
    else:
        message = "Please use the format yyyy-mm-dd hh:mm Continent/City"
    await ctx.send(message)


@bot.command(name="local",help="yyyy-mm-dd hh:mm timezone:Continent/City - converts UTC to your Timezone, works in bot channel", pass_context=True)
async def local(ctx, date, time, zone):
    chan = ctx.message.channel.id
    if checksetting(conn, 'bot', chan):
        if time != "" and zone != "":
            if date == "today":
                date = utcToday()
            message = toLocal(date, time, zone)
        else:
            message = "Please use the format yyyy-mm-dd hh:mm Continent/City"
        await ctx.send(message)
    else:
        await ctx.message.delete()

@bot.command(name='info',help='gives info on essential KOAI concepts',pass_context=True)
async def raid(ctx, theme = ""):
    message = help(help_items, theme)
    await ctx.message.delete()
    await ctx.send(message)


@bot.command(name='setpref', help='sets a new prefix for bot',pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def setpref(ctx, prefix):
    setprefix(conn,prefix)
    x = getprefix(conn)
    bot.command_prefix = x
    await ctx.message.delete()
    message = "Prefix is set to "+x
    await ctx.send(message)


@bot.command(name='dragon', help='sets a new prefix for bot',pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def dragon(ctx, handle):
    if handle == "start":
        game = "True"
        message = "Let the game begin! "
        bot.isgame = True
    elif handle == "stop":
        game = "False"
        bot.isgame = False
        message = "The game was stopped"
    setgame(conn,game)


    await ctx.message.delete()

    await ctx.send(message)

@bot.command(name='addlang', help='sets language channel',pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def addlang(ctx, language):
    chan = ctx.channel.id
    print(chan)
    addlanguage(conn,language,chan)
    await ctx.message.delete()


@bot.command(name='flip', help='flips a coin',pass_context=True)
async def flip(ctx):
    chan = ctx.message.channel.id
    if checksetting(conn, 'bot', chan):
        await ctx.send(coin())


@bot.command(name='rand', help='flips a coin',pass_context=True)
async def ran(ctx, number, amount = 1):
    chan = ctx.message.channel.id
    if checksetting(conn, 'bot', chan):
        await ctx.send(rannum(int(number),int(amount)))

@bot.command(name = 'inquire', help="Works from dm only, allows you to message keepers, put the message into quotes",pass_context=True)
async def inquire(ctx, message):
    if not ctx.guild:
        sender = ctx.author.mention
        keep = bot.get_channel(bot.keepers)
        await keep.send(sender+" "+message)
        await ctx.send("Thank you! The Keepers will read your message as soon as possible and contact you if necessary")
    else:
        await ctx.send("This is a DM-only command")




@bot.event
async def on_raw_reaction_add(payload):
    chan = payload.channel_id
    print(checksetting(conn,'accountability', chan))
    if checksetting(conn,'accountability', chan):
        if payload.emoji.name == "📌":
            msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            await msg.pin()
        elif payload.message_id == bot.raid_id and bot.raidstatus == 1 and payload.emoji.name == "⚔" and payload.member.bot == False:
            print("it's alive")
            looper.start()
            bot.raidstatus = 2
            channel = bot.get_channel(bot.account_id)
            raider = await channel.fetch_message(bot.raid_id)
            remain = "```RAID IS BEGINNING: "+str(bot.raidlen-bot.minutes+1)+" MINUTES TO GO```"
            raidlist = ""
            for i in bot.raid_members:
                raidlist = raidlist+str(i)+"; "
            print(raidlist)
            bot.current_raid.amnt = len(bot.raid_members)
            bot.current_raid.mmbr = raidlist
            await channel.send("```RAID HAS STARTED!```")
            await raider.edit(content=remain)
        elif payload.message_id == bot.raid_id and bot.raidstatus == 1 and payload.emoji.name == "🗡" and payload.member.bot == False:
            bot.raid_members.append(payload.member.id)
            if getuserval(conn,payload.member.id):
                bot.current_raiders[str(payload.member.id)]=(getuserval(conn, payload.member.id))
                print("exist")
            else:
                bot.current_raiders[str(payload.member.id)]=(Pommer(str(payload.member.id), 50))
                print("new")
        elif payload.message_id == bot.raid_id and bot.raidstatus == 1 and payload.emoji.name == "💤" and payload.member.bot == False:
            print("it's alive")
            looper.start()
            bot.raidstatus = 2
            channel = bot.get_channel(bot.account_id)
            raider = await channel.fetch_message(bot.raid_id)
            remain = "```BREAK WAS STARTED: " + str(bot.raidlen - bot.minutes + 1) + " MINUTES REMAINING```"
            await raider.edit(content=remain)
        elif payload.message_id == bot.raid_id and bot.raidstatus == 1 and payload.emoji.name == "🛏️" and payload.member.bot == False:
            bot.raid_members.append(payload.member.id)
        elif payload.message_id == bot.congrats and bot.raidstatus == 4 and payload.emoji.name in ["🗡", "🛡️", "💊", "⛏", "💣","❓"] and payload.member.bot == False:
            player = payload.member.id
            bot.raid_members.remove(player)
            raider = bot.current_raiders[str(player)]

            print(raider.poms+"t")
            print("________________")
            print(raider.total)
            raider.total+=1
            raider.poms = line_update(raider.poms)
            print(raider.total, raider.poms)
            bot.raider_actions[raider.user] = payload.emoji.name
            bot.current_raiders[str(payload.member.id)] = raider


            if len(bot.raid_members) ==0:
                damage = 0
                print(bot.current_raid.stamp, bot.current_raid.mmbr)
                print("__________________")
                selector = []
                for i in bot.current_raiders:
                    bot.current_raiders[i].ac = 15
                    selector.append(bot.current_raiders[i].user)
                for i in bot.current_raiders:
                    user = bot.current_raiders[i].user

                    command = getaction(bot.raider_actions[i])
                    if command in ["sword", "axe", "fire"]:
                        result = bot.current_raiders[i].action(command, bot.current_raid.ac)
                        print(result," RESULT")
                        damage += result[0]
                    elif command == "defence":
                        ln = len(bot.current_raiders)
                        nm = min(3, max(ln//3, 1))
                        lst = ranpop(nm, ln)
                        print("LST: ", lst)
                        for j in lst:
                            print("I: ",j)
                            bot.current_raiders[selector[j]].action("defence",1)
                    elif command == "heal":
                        for j in bot.current_raiders:
                            bot.current_raiders[j].action("heal", 0)
                    print(str(bot.current_raiders[i]))
                    setuserval(conn, bot.current_raiders[i])


                print("__________________")
                bot.current_raid.bhp-=damage
                print("hp: ", bot.current_raid.bhp)
                setraidstat(conn, bot.current_raid)
                bot.raidstatus = 0
                bot.raider_actions = {}
                bot.current_raiders = {}










@bot.event
async def on_raw_reaction_remove(payload):
    chan = payload.channel_id
    if checksetting(conn,'accountability', chan):
        if payload.emoji.name == "📌":
            print("emoji_removed")
            msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            await msg.unpin()
        elif payload.message_id == bot.raid_id and (bot.raidstatus == 2 or bot.raidstatus == 1)  and payload.emoji.name == "🗡" :
            raidmsg = await bot.get_channel(chan).fetch_message(bot.raid_id)
            reacs = raidmsg.reactions
            raiders = []
            for i in reacs:
                if i.emoji == "🗡":
                    async for user in i.users():
                        raiders.append(user.id)
            print(raiders)
            for i in bot.raid_members:
                if i not in raiders:
                    bot.raid_members.remove(i)

            if bot.raid_members == []:
                print(bot.raid_members)
                looper.cancel()




@bot.event
async def on_message(message):
    hug = get(bot.emojis, name='BlobHug')
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
    if checksetting(conn, "discussion", chan):
        if ":BlobHug:" in line:
            bot.hug_counter += 1
            bot.hug_breaker = 0
        else:
            bot.hug_breaker = min(4, bot.hug_breaker+1)
        if bot.hug_breaker > 3:
            bot.hug_counter = 0
        if bot.hug_counter ==5:
            response =str(hug)
            bot.hug_counter = 0
            await message.channel.send(response)

    await bot.process_commands(message)


@bot.event
async def on_member_update(before, after):
    if len(before.roles) < len(after.roles):
        newRole = next(role for role in after.roles if role not in before.roles)
        if checkrole(newRole.name):
            chan = (roletochan(conn,newRole.name))
            print(chan)
            if chan != -1:
                channel = bot.get_channel(chan)
                await channel.send("{0} joined {1}".format(after.mention, channel.mention))


@tasks.loop(minutes=1, count=100)
async def looper():
    if bot.minutes == bot.raidlen:
        print('DONE')
        looper.stop()
    print(bot.minutes)
    print(str(bot.raid_id), bot.account_id, "raid")
    channel = bot.get_channel(bot.account_id)
    if bot.minutes > 0:
        raider = await channel.fetch_message(bot.raid_id)
        if (bot.raidlen-bot.minutes) != 1:
            mins = " MINUTES"
        else:
            mins = " MINUTE"
        if bot.raidbreak:
            remain = "```RAID HAS "+str(bot.raidlen-bot.minutes)+mins+" TO GO```"
        else:
            remain = "```BREAK HAS "+str(bot.raidlen-bot.minutes)+" MINUTES TO GO```"
        await raider.edit(content = remain)
    bot.minutes += 1





@looper.after_loop
async def raid_done():
    print("raid done")
    bot.minutes = 0
    channel = bot.get_channel(bot.account_id)
    if bot.raidbreak:
        if bot.raid_members != []:
            message = "RAID DONE!!!\n Congratulations to "
            for user in bot.raid_members:
                member = await bot.fetch_user(user)
                name = member.mention
                message = message + name +", "
            message = message[:-2]+"!"
            sent = await channel.send(message)
            if bot.isgame:
                await sent.add_reaction("🗡")
                await sent.add_reaction("🛡️")
                await sent.add_reaction("💊")
                if len(bot.raid_members)>3:
                    await sent.add_reaction("⛏")
                if len(bot.raid_members)>5:
                    await sent.add_reaction("💣")
                if len(bot.raid_members)>7:
                    await sent.add_reaction("❓")
                bot.congrats = sent.id
                bot.raidstatus = 4
            else:
                bot.raidstatus = 0
            bot.current_raid.stamp = currentUTC()



        else:
            message = "Sorry, everyone left"
            await channel.send(message)



    else:
        message = "BREAK FINISHED!!!\n Let's go back to work, "
        for user in bot.raid_members:
            member = await bot.fetch_user(user)
            name = member.mention
            message = message + name + ", "
        message = message[:-2] + "!"
        await channel.send(message)
    sent = await channel.fetch_message(bot.raid_id)
    print(sent.content)
    await sent.unpin()
    bot.on_raid = False





@bot.command(name = "event", help = "Adds an event",pass_context=True)
@commands.has_any_role(ADMIN_ROLE, EVENT)
async def event(ctx, day="", time="", channel="", name=""):
    if day != "" and time != "" and channel != "" and name !="":
        num = addevent(conn,day, time, channel, name)
        await ctx.send("Your event ticket is " + str(num) + ", please keep it for the case of canceling it")
    elif day == "" and time == "" and channel == "" and name =="":
        ev = geteventlist(conn)
        message = ""
        for i in ev:
            line = str(i[0])+": "+str(i[1])+" "+str(i[2]).rsplit(sep=':',maxsplit=1)[0]+" "+ str(i[3]) + " "+i[4]+"\n"
            message += line
        await ctx.send(message)


@bot.command(name = "delevent", help = "Deletes an event",pass_context=True)
@commands.has_any_role(ADMIN_ROLE, EVENT)
async def delevent(ctx, ticket):
    remevent(conn, int(ticket))
    await ctx.send("Ticket "+ticket+" was removed")



@bot.command(name = "schedule", help = "Show events converted to your timezone", pass_context = True)
async def schedule(ctx, zone = "UTC"):
    chan = ctx.message.channel.id
    if checksetting(conn, 'bot', chan):
        ev = convertlist(conn, geteventlist(conn),zone)
        message = ""
        today = getToday(zone)
        toddate = datetime.datetime.strptime(today,"%Y-%m-%d")
        stamp_list = [toddate + datetime.timedelta(days=x) for x in range(8)]
        date_list = []
        for i in stamp_list:
            date_list.append(i.date())
        print(date_list)
        for i in ev:
            print(i)
            if i[1] in date_list and  i[2].hour > datetime.datetime.utcnow().time().hour or (i[2].hour == datetime.datetime.utcnow().time().hour and i[2].minute >= datetime.datetime.utcnow().time().minute):
                if i[3] != -1:
                    channel = bot.get_channel(i[3])
                else:
                    channel = discord.utils.get(ctx.guild.channels, name='common-room')
                line = "📖 "+ str(i[1]) + " " + str(i[2]).rsplit(sep=':', maxsplit=1)[0] + " " + channel.mention + " " + i[4] + "\n"
                message += line
        if message == "":
            message = "```No events next week, sorry```"
        else:
            message = "```THIS IS THIS WEEK'S SCHEDULE```\n"+message
        await ctx.send(message)
    await ctx.message.delete()

@tasks.loop(hours=1)
async def updater():
    hour = datetime.datetime.utcnow().time().hour
    if hour == 12:
        print(bot.get_channel(bot.common).name)
        announcements = bot.get_channel(bot.eventchan)
        message = ""
        ev = convertlist(conn, geteventlist(conn), 'UTC')
        today = getToday('UTC')
        toddate = datetime.datetime.strptime(today, "%Y-%m-%d")
        stamp_list = [toddate + datetime.timedelta(days=x) for x in range(3)]
        date_list = []
        for i in stamp_list:
            date_list.append(i.date())
        print(date_list)
        for i in ev:
            print(i)
            if i[1] in date_list and i[2].hour > 12 or (i[2].hour ==12 and i[2].minute >= datetime.datetime.utcnow().time().minute):
                if i[3] != -1:
                    channel = bot.get_channel(i[3])
                else:
                    channel = bot.get_channel(bot.common)
                line = "📖 "+ str(i[1]) + " " + str(i[2]).rsplit(sep=':', maxsplit=1)[0] + " UTC " + channel.mention + " " + i[4] + "\n"
                message += line
            elif i[1]<toddate.date():
                remevent(conn,i[0])
        print(message)
        if message != "":
            if bot.evrole :
                message = bot.evrole[0].mention +"\n```CLOSEST EVENTS```\n"+message
            else:
                message =  "```CLOSEST EVENTS```\n" + message
            await announcements.send(message)
    else:
        print("Hour is ", hour)







bot.run(TOKEN)
