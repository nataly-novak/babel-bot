import os
import random

from discord.ext import commands, tasks
import discord
from dotenv import load_dotenv
from dbwork import makedb, filldb, randomquote, removelast, addquote, settingsdb, addsetting, removesetting, checksetting, \
    setprefix, setdefaults, getprefix, quotenum, getchannel
from wordlists import getreaction, worddicts, help
from discord.utils import get
from timework import toUTC, currentUTC, toLocal, getToday, utcToday
from languages import checkrole, roletochan, addlanguage, languagedb, checkchan
from randomer import coin, rannum
from scheduler import maketimetable, addevent, geteventlist, convertlist, remevent
from pombase import makepombases, checkgame, setgame, setuserval,getuserval, setraidstat, getraidstat, getaction, cleanbases, dropbase, getwinners
from pommer import Pommer
from stamper import line_update, stamp_list
from mechanics import ranpop, roll, channeling
from raid import  Raid
from rules import ruleprint
from vars import *

import os
import psycopg2
import pytz
import datetime


intents = discord.Intents.all()

load_dotenv()

TOKEN = os.getenv('TOKEN')
ADMIN_ROLE = os.getenv('ADMIN_ROLE')
EVENT = os.getenv('EVENT')



#dropbase()
settingsdb()
makedb()
setdefaults()
filldb()
help_items = worddicts()
languagedb()
maketimetable()
makepombases()
#cleanbases()


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
bot.isgame = checkgame()
bot.congrats = 0
bot.current_raid = getraidstat()
bot.current_raiders = {}
bot.raider_actions = {}
bot.damagers = []
bot.guild = None
bot.debuf_counter = 0

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
    bot.guild = bot.guilds[0]
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
    if times.isdecimal():
        if int(times) <= 50:
            chan = ctx.message.channel.id
            if checksetting('accountability', chan):
                if bot.on_raid == False:
                    if checkgame():
                        if len(bot.raid_members) != 0:
                            await game_process()
                            bot.raid_members = []
                    bot.raidlen = int(times)
                    message = "```WAITING FOR RAID OF " +times+  " MINUTES TO START.....\n To join the raid, click shield emoji. \n When everyone is ready, someone should click sword emoji to start the timer\n This message will be updated as a timer. \n You will see the timer in the pinned message```"
                    sent = await ctx.send(message)
                    bot.account_id = ctx.message.channel.id
                    await ctx.message.delete()
                    bot.raid_id = sent.id
                    await sent.pin()
                    bot.on_raid = True
                    bot.raidbreak = True
                    await sent.add_reaction("🛡️")
                    await sent.add_reaction("🗡")
                    bot.raidstatus = 1
                    if getraidstat():
                        bot.current_raid = getraidstat()
                else:
                    message = "TIMER IS ALREADY ON, SEE PINNED MESSAGES"
                    await ctx.send(message)
                    await ctx.message.delete()
        else:
            await ctx.send("The time is too long. It is highly advised to do focused work in a reasonable durations of time, please enter the shorter duration")
    else:
        await ctx.send("I am sorry, but your input is unreadable. You can type ;raid without parameters for a standard one.")






@bot.command(name='cancel', help='cancels raid',pass_context = True)
async def cancel(ctx):
    if bot.raidstatus ==1:
        bot.on_raid = False
        bot.raidstatus = 0
        bot.raid_members = []
        bot.current_raiders = {}
        await ctx.send("```THE RAID WAS CANCELED```")


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

@bot.command(name='info',help='gives info on essential KOAI concepts',pass_context=True)
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
    setgame(game)


    await ctx.message.delete()

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
        elif payload.message_id == bot.raid_id and bot.raidstatus == 1 and payload.emoji.name == "🗡" and payload.member.bot == False and payload.member.id in bot.raid_members:
            bot.current_raid = getraidstat()
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
        elif payload.message_id == bot.raid_id and bot.raidstatus == 1 and payload.emoji.name == "🛡️" and payload.member.bot == False:
            bot.raid_members.append(payload.member.id)
            if getuserval(payload.member.id):
                bot.current_raiders[str(payload.member.id)]=(getuserval(payload.member.id))
                print("exist")
            else:
                bot.current_raiders[str(payload.member.id)]=(Pommer(str(payload.member.id)))
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
        elif payload.message_id == bot.congrats and bot.raidstatus == 4 and payload.emoji.name in ["🗡", "🛡️", "💊", "🪓", "💣","❓"] and payload.member.bot == False:
            if payload.emoji.name != "❓" or bot.debuf_counter == 0:
                player = payload.member.id
                bot.raid_members.remove(player)
                raider = bot.current_raiders[str(player)]
                if payload.emoji.name == "❓":
                    bot.debuf_counter = 1
            else:
                channel = bot.get_channel(bot.account_id)
                await channel.send(payload.member.mention + " the debuff was already used, chose another emoji\n")

            print(raider.poms+"t")
            print("________________")
            print(raider.total)
            raider.total+=1
            raider.poms = line_update(raider.poms)
            print(raider.total, raider.poms)
            bot.raider_actions[raider.user] = payload.emoji.name
            bot.current_raiders[str(payload.member.id)] = raider


            if len(bot.raid_members) ==0:
                await game_process()








@bot.command(name="mystat", help ="shows your current hp, defence and status", pass_context = True)
async def mystat(ctx):
    player = (ctx.author.id)
    print(player)
    raider = getuserval(player)
    if raider != None:
        hp = (raider.hp)
        ac = raider.ac
        if raider.staggered == 2:
            if len(stamp_list(raider.poms))<17:
                stagger = ", You can act freely "
            else:
                stagger = ", You are too tired to act"
        else:
            stagger = ", You cannot act, though you can still receive heals and defences"
    else:
        hp = player_hp
        ac = player_ac
        stagger = ", You can act freely "
    message = ctx.author.mention+", Your hp is " + str(hp)+", Your defence is "+ str(ac) + stagger
    await ctx.send(message)


@bot.command(name='showleaders', help='shows current event leaders',pass_context=True)
@commands.has_role(ADMIN_ROLE)
async def showleaders(ctx):
    message = ""
    nominations = ["Total Poms", "Best Healer", "Best Damage", "Best Defender"]
    lst = getwinners()
    for i in range(len(lst)):
        message = message+nominations[i]+":\n"
        for j in lst[i]:
            memb = bot.guild.get_member(int(j[0].rstrip()))
            if memb.nick:
                name = memb.nick
            else:
                name = memb.name
            message = message + name + ": "+ str(j[1])+"\n"
        message= message+"------------------\n"
    await ctx.send("```"+message+'```')




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
                    bot.current_raiders.pop(str(i), None)

            for i in bot.current_raiders:
                print(i)

            if bot.raid_members == []:
                print(bot.raid_members)
                looper.cancel()
                print("CANCELATION")




@bot.event
async def on_message(message):
    hug = get(bot.emojis, name='BlobHug')
    chan = message.channel.id
    line = message.content
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
            message = message+ "\n`Sword emoji is for attack, Shield emoji defends some ot the raid members, Pill emoji heals the raid.`\n"
            if len(bot.raid_members) > 2:  # should be 2
                message = message +"`Axe emoji gives you a stronger attack`\n"
            if len(bot.raid_members) > 6:  # should be 2
                message = message +"`Bomb emoji gives you a stronger attack that hits more often`\n"
            if len(bot.raid_members) > 2:  # should be 2
                message = message +"`Question mark emoji launches a mystery attack that weakens the dragon in some way`\n"
            sent = await channel.send(message)
            if bot.isgame:
                await sent.add_reaction("🗡")
                await sent.add_reaction("🛡️")
                await sent.add_reaction("💊")
                if len(bot.raid_members)>0: #should be 2
                    await sent.add_reaction("🪓")
                if len(bot.raid_members)>0: #should be 4
                    await sent.add_reaction("💣")
                if len(bot.raid_members)>0: #should be 6
                    await sent.add_reaction("❓")
                bot.congrats = sent.id
                bot.raidstatus = 4
            else:
                bot.raidstatus = 0
            bot.current_raid.stamp = currentUTC()



        else:
            message = "```Sorry, everyone left```"
            await channel.send(message)
            bot.raidstatus = 0



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



async def game_process():
    message = ""
    damage = 0
    bot.current_raid.vhp = min(bot.current_raid.vhp, 500)
    print(bot.current_raid.stamp, bot.current_raid.mmbr)
    print("__________________")
    selector = []

    if bot.current_raid.effect != "":
        bot.current_raid.effect = ""
    bot.current_raid.bab = dragon_bab
    bot.current_raid.damage = dragon_damage
    bot.current_raid.ac = dragon_ac
    for i in bot.current_raiders:
        if bot.current_raiders[i].hp > player_hp:
            bot.current_raiders[i].hp = player_hp
        bot.current_raiders[i].ac = 15
        selector.append(bot.current_raiders[i].user)
        print("RAIDER",bot.current_raiders[i].user)
        if bot.current_raiders[i].hp == 0:
            bot.current_raiders[i].staggered = 0
    print(selector)

    for i in bot.current_raiders:
        if i in bot.raider_actions:
            if bot.current_raiders[i].staggered == 2:
                command = getaction(bot.raider_actions[i])
                if len(stamp_list(bot.current_raiders[i].poms))<17:
                    if command == "debuff":
                        user = bot.guild.get_member(int(bot.current_raiders[i].user))
                        if user.nick:
                            name = user.nick
                        else:
                            name = user.name
                        message = message + name + " uses the mysterious attack!"+bot.current_raid.mystery()
                        bot.damagers.append([20, bot.current_raiders[i].user])
                        print("BOT DAMAGERS", bot.damagers)
                else:
                    user = bot.guild.get_member(int(bot.current_raiders[i].user))
                    if user.nick:
                        name = user.nick
                    else:
                        name = user.name
                    message = message+ name + " worked too much and is too tired to do anything"
                    bot.damagers.append([0, bot.current_raiders[i].user])
                    bot.raider_actions[i] = "❓"
                    if bot.current_raiders[i].staggered == 2:
                        bot.current_raiders[i].staggered = 0

    for i in bot.current_raiders:
        if i in bot.raider_actions:
            user = bot.guild.get_member(int(bot.current_raiders[i].user))
            if user.nick:
                name = user.nick
            else:
                name = user.name
            today_raids = len(stamp_list(bot.current_raiders[i].poms))
            if today_raids < 5:
                multiplier = 1
            else:
                multiplier = (13-(today_raids-4))/13
            if today_raids < 9:
                heal_multiplier = 1
            else:
                heal_multiplier = (9-(today_raids-4))/9

            if bot.current_raiders[i].staggered == 2:
                command = getaction(bot.raider_actions[i])
                if command in ["sword", "axe", "bomb"]:
                    add = len(selector) - 1
                    result = bot.current_raiders[i].action(command, bot.current_raid.ac, add)
                    print(result, " RESULT")
                    if result[0] != 0:
                        result[0] = max(int(result[0]*multiplier),1)
                    print(result, " RESULT")
                    damage += result[0]
                    bot.current_raiders[i].dealed+= result[0]
                    bot.damagers.append([result[0], bot.current_raiders[i].user])
                    print("BOT DAMAGERS",bot.damagers)
                    message = message + name + " uses " + command + ". It's a " + result[1] + " with " + str(result[0]) + " damage\n"
                elif command == "defence":
                    if today_raids <9:
                        defval = 2
                    else:
                        defval = 1
                    bot.current_raiders[i].done +=defval
                    ln = len(bot.current_raiders)
                    nm = min(max_shields, max(ln // 3, 1))
                    lst = ranpop(nm, ln)
                    print("LST: ", ln, nm, lst)
                    lst = ranpop(nm, ln)
                    defs = ""
                    for j in lst:
                        print("I: ", j)
                        bot.current_raiders[selector[j]].action("defence", defval)
                        defended = bot.guild.get_member(int(selector[j]))
                        if defended.nick:
                            def_name = defended.nick
                        else:
                            def_name = defended.name
                        defs = defs + def_name + ", "
                    bot.damagers.append([3, bot.current_raiders[i].user])
                    print("BOT DAMAGERS", bot.damagers)
                    message = message + name + " uses " + command + " to defend " + defs + " it increases their defence by "+str(defval)+"\n"

                elif command == "heal":
                    healamount = max(int(channeling()*heal_multiplier),1)
                    bot.current_raiders[i].healed +=healamount
                    for j in bot.current_raiders:
                        bot.current_raiders[j].action("heal", healamount)
                    message = message + name + " uses " + command + " to heal " + str(healamount) + " hp to everyone!\n"
                    bot.damagers.append([healamount, bot.current_raiders[i].user])
                    print("BOT DAMAGERS", bot.damagers)
                print(str(bot.current_raiders[i]))
            else:
                bot.damagers.append([0, bot.current_raiders[i].user])
                message = message + name + " is staggered and can't do anything\n"
        else:
            user = bot.guild.get_member(int(bot.current_raiders[i].user))
            if user.nick:
                name = user.nick
            else:
                name = user.name
            bot.damagers.append([0, bot.current_raiders[i].user])
            bot.current_raiders[i].staggered = 1
            message = message + name + " seems to be staggered and can't do anything\n"
    useless = 0
    destruction = False
    if bot.current_raid.effect != "stagger":
        print("------\nTHE DRAGON ATTACKS\n-----")
        if len(bot.damagers) >0:
            print("------\nDAMAGERS NOT NULLn-----")
            print("BOT DAMAGERS", bot.damagers)
            for i in bot.current_raiders:
                if bot.current_raiders[i].staggered < 2:
                    useless += 1
            print(useless)
            if useless > len(bot.current_raiders) // 2:
                destruction = True
                print("TRUUUUU")
            if not destruction:
                if bot.current_raid.trg > 0:
                        if len(bot.damagers) > 1:
                            n = roll(len(bot.damagers) //2)
                            if n//2<1:
                                atk = [0]
                            else:
                                thres = n//2-1
                                add = roll(n - thres)
                                atk = ranpop(add+thres, n)
                        else:
                            atk = [0]
                        print(atk)
                        bot.damagers.sort(reverse=True)
                        for i in atk:
                            damaged = bot.current_raiders[bot.damagers[i][1]]
                            defended = bot.guild.get_member(int(damaged.user))
                            if defended.nick:
                                def_name = defended.nick
                            else:
                                def_name = defended.name
                            dam = bot.current_raid.physical(damaged.ac)
                            res = bot.current_raiders[bot.damagers[i][1]].suffer(dam[0])
                            print("RESULT ", res)
                            print(str(bot.current_raiders[bot.damagers[i][1]]))
                            message = message + "Dragon attacks " + def_name + "! It's a " + dam[1] + " with " + str(
                                dam[0]) + " damage!\n"
                        bot.current_raid.trg -= 1
                else:
                    message = message + "Dragon uses it's breath!\n"
                    print("breath attack")
                    print(selector)
                    for i in selector:
                        staggered = roll(2)
                        if staggered == 2:
                            bot.current_raiders[i].staggered = -1
                            print("Staggered", i)
                            defended = bot.guild.get_member(int(bot.current_raiders[i].user))
                            if defended.nick:
                                def_name = defended.nick
                            else:
                                def_name = defended.name
                            message = message + def_name + " is staggered for the next round\n"
                        else:
                            print("Evaded", i)
                            defended = bot.guild.get_member(int(bot.current_raiders[i].user))
                            if defended.nick:
                                def_name = defended.nick
                            else:
                                def_name = defended.name
                            message = message + def_name + " evaded the dragon's fire!\n"
                        bot.current_raid.trg = roll(breath_roll) + breath_cooldown
            else:
                res = bot.current_raid.burn()
                print("Burned", res)
                message = message + "The dragon uses it's breath on the village and deals " + str(res[0]) + " damage. " + str(bot.current_raid.vhp) + " hp remains\n"
            for i in bot.current_raiders:
                bot.current_raiders[i].staggered = min(2, bot.current_raiders[i].staggered + 2)
                setuserval(bot.current_raiders[i])
        else:
            message = message + "Something went wrong\n"
    else:
        message = message + "The dragon did nothing due to your action \n"

    print("__________________")
    mult = 1
    if bot.current_raid.effect == "vulnerable":
        mult = 1.5
    bot.current_raid.bhp -= mult*damage
    if bot.current_raid.bhp<0:
        bot.current_raid.bhp = 0
    message = message + "The dragon has " + str(bot.current_raid.bhp) + " HP\n"
    if bot.current_raid.bhp == 0:
        message = message + "THE DRAGON WAS DEFEATED! CONGRATULATIONS!\n"



    print(str(bot.current_raid))
    setraidstat( bot.current_raid)
    bot.raidstatus = 0
    bot.raider_actions = {}
    bot.current_raiders = {}
    bot.damagers = []
    protocol = bot.get_channel(getchannel("game"))
    await protocol.send(message)
    bot.debuf_counter = 0



bot.run(TOKEN)
