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




