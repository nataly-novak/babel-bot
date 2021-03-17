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
from rules import ruleprint

import os
import psycopg2
import pytz
import datetime

intents = discord.Intents.all()

load_dotenv()

TOKEN = os.getenv('TOKEN')
ADMIN_ROLE = os.getenv('ADMIN_ROLE')
EVENT = os.getenv('EVENT')






settingsdb()
makedb()
setdefaults()
filldb()
help_items = worddicts()
languagedb()
maketimetable()


bot = commands.Bot(command_prefix=(getprefix()),intents=intents)



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
                addlanguage(channel.name, channel.id)
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


@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        print(channel.name)
        if checkchan(channel.name):
            print(channel.name)
            addlanguage(channel.name, channel.id)
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


@bot.command(name='quote', help="generates random quotes with translation", pass_context=True)
async def cookin(ctx):
    chan = ctx.message.channel.id
    if checksetting('bot', chan):
        response = randomquote()
        await ctx.send(response)
    await ctx.message.delete()


@bot.command(name='add', help='Adds a quote. Use quotes around both quote and translation', pass_context=True)
async def itl(ctx, language, line, trans=""):
    chan = ctx.message.channel.id
    if checksetting('bot', chan):
        message = addquote(language, line, trans)
        await ctx.send(message)


@bot.command(name='del', help='deletes last quote', pass_context=True)
async def de(ctx):
    chan = ctx.message.channel.id
    if checksetting('bot', chan):
        await ctx.message.delete()
        message = removelast()
        await ctx.send(message)


@bot.command(name='quotenumber', help='Shows the current number of quotes', pass_context=True)
async def quotenumber(ctx):
    chan = ctx.message.channel.id
    if checksetting('bot', chan):
        await ctx.message.delete()
        message = quotenum()
        await ctx.send(message)

@bot.command(name='rules', help='Prints rules in chosen language (or english if no translation provided)', pass_context=True)
async def rules(ctx, language):
    await ctx.message.delete()
    message = ruleprint(language)
    resps = message.split(sep="\n")
    mes = ""
    for i in resps:
        mes = mes +i +"\n"
        print(i)
        print(mes)
        print(len(mes))
        if len(mes) >1500:
            await ctx.send(mes)
            mes = ""
    await ctx.send(mes)



@bot.command(name='addfunction', help='sets the channel for function', pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def addfunction(ctx, function):
    chan = ctx.channel.id
    print(chan)
    addsetting(function,str(chan))
    await ctx.message.delete()


@bot.command(name='delfunction', help='removes the channel from the function list', pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def delfunction(ctx, function):
    chan = ctx.channel.id
    print(chan)
    removesetting(function,str(chan))
    await ctx.message.delete()


@bot.command(name='invite',help='prints the invite you need',pass_context=True)
async def invite(ctx, invite = "default"):
    if invite == "default":
        message = "Want to invite a friend? Use this link: "
    elif invite == "partner":
        message = "Do you want to join the partner server, too? Use this link: "
    await ctx.message.delete()
    await ctx.send(message)


@bot.command(name='raid',help='prints link to raid room',pass_context=True)
async def raid(ctx, times = '25'):
    chan = ctx.message.channel.id
    if checksetting('accountability', chan):
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
            await sent.add_reaction("🛡️")
            await sent.add_reaction("🗡️")
            bot.raidstatus = 1

        else:
            message = "TIMER IS ALREADY ON, SEE PINNED MESSAGES"
            await ctx.send(message)
            await ctx.message.delete()

@bot.command(name='break',help='prints link to raid room',pass_context=True)
async def breaks(ctx, times = '5'):
    chan = ctx.message.channel.id
    if checksetting('accountability', chan):
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
    if checksetting( 'bot', chan):
        if time != "" and zone != "":
            if date == "today":
                date = utcToday()
            message = toLocal(date, time, zone)
        else:
            message = "Please use the format yyyy-mm-dd hh:mm Continent/City"
        await ctx.send(message)
    else:
        await ctx.message.delete()

@bot.command(name='info',help='gives info on essential concepts',pass_context=True)
async def raid(ctx, theme = ""):
    message = help(help_items, theme)
    await ctx.message.delete()
    await ctx.send(message)


@bot.command(name='setpref', help='sets a new prefix for bot',pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def setpref(ctx, prefix):
    setprefix(prefix)
    getprefix()
    x = getprefix()
    bot.command_prefix = x
    await ctx.message.delete()
    message = "Prefix is set to "+x
    await ctx.send(message)


@bot.command(name='addlang', help='sets language channel',pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def addlang(ctx, language):
    chan = ctx.channel.id
    print(chan)
    addlanguage(language,chan)
    await ctx.message.delete()


@bot.command(name='flip', help='flips a coin',pass_context=True)
async def flip(ctx):
    chan = ctx.message.channel.id
    if checksetting('bot', chan):
        await ctx.send(coin())


@bot.command(name='rand', help='gives several random numbers in a range. First number is range, second is the number of winners',pass_context=True)
async def ran(ctx, number, amount = 1):
    chan = ctx.message.channel.id
    if checksetting( 'bot', chan):
        await ctx.send(rannum(int(number),int(amount)))

@bot.command(name = 'inquire', help="Works from dm only, allows you to message keepers, put the message into quotes",pass_context=True)
async def inquire(ctx, message):
    is_member = False
    for guild in bot.guilds:
        if guild.get_member(ctx.author.id):
            print("incoming from member")
            is_member = True
    if is_member:
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
    print(checksetting('accountability', chan))
    if checksetting('accountability', chan):
        if payload.emoji.name == "📌":
            msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            await msg.pin()
        elif payload.message_id == bot.raid_id and bot.raidstatus == 1 and payload.emoji.name == "🗡️" and payload.member.bot == False:
            print("it's alive")
            looper.start()
            bot.raidstatus = 2
            channel = bot.get_channel(bot.account_id)
            raider = await channel.fetch_message(bot.raid_id)
            remain = "```RAID IS BEGINNING: "+str(bot.raidlen-bot.minutes+1)+" MINUTES TO GO```"
            await channel.send("```RAID HAS STARTED!```")
            await raider.edit(content=remain)
        elif payload.message_id == bot.raid_id and bot.raidstatus == 1 and payload.emoji.name == "🛡️" and payload.member.bot == False:
            bot.raid_members.append(payload.member.id)
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





@bot.event
async def on_raw_reaction_remove(payload):
    chan = payload.channel_id
    if checksetting('accountability', chan):
        if payload.emoji.name == "📌":
            print("emoji_removed")
            msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            await msg.unpin()
        elif payload.message_id == bot.raid_id and (bot.raidstatus == 2 or bot.raidstatus == 1)  and payload.emoji.name == "🛡️" :
            raidmsg = await bot.get_channel(chan).fetch_message(bot.raid_id)
            reacs = raidmsg.reactions
            raiders = []
            for i in reacs:
                if i.emoji == "🛡️":
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
    print(getreaction(line,chan))
    emo = getreaction(line,chan)
    for i in emo:
        print(i)
        if i[:1] == ':':
            em = i[1:-1]
            emoji = get(bot.emojis, name=em)
            if emoji:
                await message.add_reaction(emoji)
        else:
            await message.add_reaction(i)
    if checksetting( "discussion", chan):
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
            chan = (roletochan(newRole.name))
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
        else:
            message = "Sorry, everyone left"
        await channel.send (message)
        bot.raid_members = []

    else:
        message = "BREAK FINISHED!!!\n Let's go back to work, "
        for user in bot.raid_members:
            member = await bot.fetch_user(user)
            name = member.mention
            message = message + name + ", "
        message = message[:-2] + "!"
        await channel.send(message)
        bot.raid_members = []
    sent = await channel.fetch_message(bot.raid_id)
    print(sent.content)
    await sent.unpin()
    bot.on_raid = False
    bot.raidstatus = 0



@bot.command(name = "event", help = "Adds an event",pass_context=True)
@commands.has_any_role(ADMIN_ROLE, EVENT)
async def event(ctx, day="", time="", channel="", name=""):
    if day != "" and time != "" and channel != "" and name !="":
        num = addevent(day, time, channel, name)
        await ctx.send("Your event ticket is " + str(num) + ", please keep it for the case of canceling it")
    elif day == "" and time == "" and channel == "" and name =="":
        ev = geteventlist()
        message = ""
        for i in ev:
            line = str(i[0])+": "+str(i[1])+" "+str(i[2]).rsplit(sep=':',maxsplit=1)[0]+" "+ str(i[3]) + " "+i[4]+"\n"
            message += line
        if message =="":
            message = "Empty schedule"
        await ctx.send(message)


@bot.command(name = "delevent", help = "Deletes an event",pass_context=True)
@commands.has_any_role(ADMIN_ROLE, EVENT)
async def delevent(ctx, ticket):
    remevent(int(ticket))
    await ctx.send("Ticket "+ticket+" was removed")



@bot.command(name = "schedule", help = "Show events converted to your timezone", pass_context = True)
async def schedule(ctx, zone = "UTC"):
    chan = ctx.message.channel.id
    if checksetting( 'bot', chan):
        ev = convertlist( geteventlist(),zone)
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
            if i[1] in date_list and  (i[2].hour > datetime.datetime.utcnow().time().hour or (i[2].hour == datetime.datetime.utcnow().time().hour and i[2].minute >= datetime.datetime.utcnow().time().minute) or i[1] != date_list[0]):
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
        ev = convertlist(geteventlist(), 'UTC')
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
                remevent(i[0])
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
