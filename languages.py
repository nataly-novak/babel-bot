import psycopg2
from dbwork import getconn

roles = ['American Sign Language', 'Arabic', 'Czech', 'Danish', 'Dutch', 'English', 'Esperanto', 'Filipino', 'French', 'German', 'Greek', 'Hebrew', 'Indonesian', 'Hindi'     ,'Italian', 'Japanese','Korean','Latin', 'Mandarin', 'Portuguese', 'Russian','Spanish', 'Swedish', 'Turkish','Vietnamese']
chans = ['american-sign-language', 'arabic', 'czech', 'danish', 'dutch', 'english', 'esperanto', 'filipino', 'french', 'german', 'greek', 'hebrew', 'indonesian', 'hindustani','italian', 'japanese','korean','latin', 'mandarin', 'portuguese', 'russian','spanish', 'swedish', 'turkish','vietnamese']

def languagedb():
    conn = getconn()
    cur = conn.cursor()
    print('languages')
    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('languages',))
    check = (cur.fetchone()[0])
    print(check)
    if not check:
        cur.execute('''CREATE TABLE languages (
                    NMB INT NOT NULL,
                    LANG CHAR(30) NOT NULL,
                    CHAN CHAR(20) NOT NULL
                    );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE languages ADD CONSTRAINT test_pkey6 PRIMARY KEY (LANG);')

    else:
        print('No need')
    conn.commit()
    cur.close
    conn.close()


def addlanguage(language, id):
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT MAX(NMB) FROM languages;")
    a = str(cur.fetchone())
    if a == '(None,)':
        ar = 0
    else:
        ar = int(a[1:-2]) + 1
    cur.execute("INSERT INTO languages VALUES (%s,%s,%s) ON CONFLICT (LANG) DO UPDATE SET CHAN = excluded.CHAN ;", (ar, language, id))
    conn.commit()
    cur.execute("SELECT NMB,LANG, CHAN from languages")
    rows = cur.fetchall()
    x = 0
    for j in rows:
        x += 1
    cur.close()
    conn.close

def getlanchan(language):
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT CHAN FROM languages WHERE LANG = %s", (language,))
    resp = str(cur.fetchone())
    chan = resp[2:-3].strip()
    if chan != "":
        id = int(chan)
    else:
        id = -1
    return id
    cur.close()
    conn.close()


def roletochan(role):
    n = roles.index(role)
    a = chans[n]
    item = a.ljust(30)
    return getlanchan(item)


def checkrole(role):
    return role in roles

def checkchan(chan):
    return chan in chans




