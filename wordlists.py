discussion = {'english': ':flag_gb:', 'japanese': ':flag_jp:', 'spanish': ':flag_es:', 'french': ':flag_fr:',
              'german': ':flag_de:', 'arabic': ':ArabLanguage:', 'mandarin': ':flag_cn: '}
quest = {"I will master": ":crossed_swords:"}
accountability = {"pom": ":tomato:"}

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
    for i in words:
        if i in line:
            emolist.append(words.get(i))
    return emolist

def getgroup(conn, id):
    if checksetting(conn, 'accountability', id):
        return 'accountability'
    elif checksetting(conn, 'quest', id):
        return 'quest'
    elif checksetting(conn, 'discussion', id):
        return 'discussion'
    else:
        return 'none'

def getreaction(conn, message, id):
    name = getgroup(conn,id)
    if name != 'none':
        return checkline(message,name)
    else:
        return []

