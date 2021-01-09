discussion = {'english': '🇬🇧', 'japanese': '🇯🇵', 'spanish': '🇪🇸', 'french': '🇫🇷',
              'german': '🇩🇪', 'arabic': ':ArabLanguage:', 'mandarin': '🇨🇳'}
quest = {"i will master": "⚔"}
accountability = {"pom": "🍅", "pomming": "🍅"}

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




