discussion = {'english': '🇬🇧', 'japanese': '🇯🇵', 'spanish': '🇪🇸', 'french': '🇫🇷',
              'german': '🇩🇪', 'arabic': ':ArabLanguage:', 'mandarin': '🇨🇳', "good morning": "🌞", "love":"😍","hug":":BlobHug:", "good night": "🌛"}
quest = {"i will master": "⚔", "reflection": "🛡️", "vow": "⚔", "i am going to": "⚔"}
accountability = {"pom": "🍅", "plan": "🗓️"}

from dbwork import checksetting


def getdict(name):
    if name == 'discussion':
        return discussion
    elif name == 'quest':
        return quest
    elif name == "accountability":
        return accountability
    else:
        return {}

def checkline(line, name):
    words = getdict(name)
    emolist = []
    line_n = line.lower()
    for i in words:
        if i in line_n:
            emolist.append(words.get(i))
    return emolist


def getgroups(conn, id):
    groups = []
    if checksetting(conn, 'accountability', id):
        groups.append('accountability')
    if checksetting(conn, 'quest', id):
        groups.append('quest')
    if checksetting(conn, 'discussion', id):
        groups.append('discussion')
    if groups == []:
        groups.append('none')
    return groups


def getreaction(conn, message, id):
    names = getgroups(conn, id)
    print(names)
    emotes = []
    for name in names:
        if name != 'none':
            print(name)
            emo = checkline(message, name)
            for j in emo:
                emotes.append(j)
    return  emotes

def worddicts():
    help = {}
    f = open("help", "r",encoding="utf8")
    f1 = f.readlines()
    for i in f1:
        line = i.rstrip().split(sep=" - ")
        help[line[0]] = line[1]
    return help

def help(help, item):
    themes = ""
    for i in help:
        themes = themes+i+", "
    themes = themes[:-2]
    if item in help:
        return item+" - "+help[item]
    elif item == "":
        return "Please specify your question. Try options like: "+ themes
    else:
        return "I do not have information about this word. Please ask the members of the server for support. I only know about: "+ themes

print(help(worddicts(),"koai"))




