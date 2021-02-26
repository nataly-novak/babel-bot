import os
import psycopg2
import random
from dotenv import load_dotenv


def getconn():
    load_dotenv()
    STAGE = os.getenv('STAGE')
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
    return conn

def settingsdb():
    conn = getconn()
    cur = conn.cursor()
    print('settingsdb')
    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('accountability',))
    check = (cur.fetchone()[0])
    print(check)
    if not check:
        cur.execute('''CREATE TABLE accountability (
            NMB INT NOT NULL,
            VAL CHAR(20) NOT NULL
            );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE accountability ADD CONSTRAINT test_pkey2 PRIMARY KEY (VAL);')
    else:
        print('No need')
    conn.commit()
    print('prefixdb')
    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('settingspref',))
    check = (cur.fetchone()[0])
    print(check)
    if not check:
        cur.execute('''CREATE TABLE settingspref (
                NMB INT NOT NULL,
                VAL CHAR(5) NOT NULL
                );''')
        print("Table created successfully")
    else:
        print('No need')
    conn.commit()
    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('discussion',))
    check = (cur.fetchone()[0])
    if not check:
        cur.execute('''CREATE TABLE discussion (
                NMB INT NOT NULL,
                VAL CHAR(20) NOT NULL
                );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE discussion ADD CONSTRAINT test_pkey3 PRIMARY KEY (VAL);')
    else:
        print('No need')
    conn.commit()
    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('quest',))
    check = (cur.fetchone()[0])
    if not check:
        cur.execute('''CREATE TABLE quest (
                NMB INT NOT NULL,
                VAL CHAR(20) NOT NULL
                );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE quest ADD CONSTRAINT test_pkey4 PRIMARY KEY (VAL);')
    else:
        print('No need')
    conn.commit()
    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('bot',))
    check = (cur.fetchone()[0])
    if not check:
        cur.execute('''CREATE TABLE bot (
                NMB INT NOT NULL,
                VAL CHAR(20) NOT NULL
                );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE bot ADD CONSTRAINT test_pkey5 PRIMARY KEY (VAL);')
    else:
        print('No need')
    conn.commit()
    cur.close()
    conn.close()





def makedb():
    conn = getconn()
    cur = conn.cursor()

    print('koai')

    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('inter',))
    check = (cur.fetchone()[0])
    if not check:
        cur.execute('''CREATE TABLE inter (
        NUM INT  NOT NULL,
        LANG CHAR (30) NOT NULL,
        QUOT CHAR(200)  NOT NULL,
        TRAN CHAR(200)
        );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE inter ADD CONSTRAINT test_pkey1 PRIMARY KEY (QUOT);')
    else:
        print('No need')
    conn.commit()
    cur.close()
    conn.close()

def filldb():
    conn = getconn()
    cur = conn.cursor()
    f = open("international", "r",encoding="utf8")
    f1 = f.readlines()
    cnt = 0
    for i in f1:
        a = i[:-1].split(' - ')
        if len(a) < 3:
            a.append('')
        cur.execute("INSERT INTO inter VALUES (%s,%s,%s,%s) ON CONFLICT (QUOT) DO NOTHING ;", (cnt, a[0], a[1], a[2]))
        cnt += 1
    cur.execute("SELECT NUM, LANG, QUOT, TRAN from inter")
    rows = cur.fetchall()
    n = len(f1)
    f.close()

def addsetting(setting, value):
    conn = getconn()
    cur = conn.cursor()
    line0 = "SELECT MAX(NMB) FROM "+setting
    cur.execute(line0)
    a = str(cur.fetchone())
    print(a)
    if a == '(None,)':
        ar = '0'
    else:
        ar = str(int(a[1:-2]) + 1)
    line1 = "INSERT INTO "+ setting + " VALUES ("+ar+","+value+") ON CONFLICT (VAL) DO NOTHING"
    cur.execute(line1)
    line2 = "SELECT NMB, VAL from "+setting
    cur.execute(line2)
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()



def removesetting(setting, value):
    conn = getconn()
    cur = conn.cursor()
    line0 = "SELECT * FROM "+setting+" FETCH FIRST ROW ONLY;"
    cur.execute(line0)
    a = str(cur.fetchone())
    b = a[1:-1].split(', ')[1]
    c = b[1:-1]
    if a != '(None,)':
        leng = len(c)
        v = ''
        for i in range(leng):
            if i<len(str(value)):
                v+=str(value)[i]
            else:
                v+=' '
        line1 = "DELETE FROM "+setting+" WHERE VAL = \'"+value+"\'"
        cur.execute(line1)
        line2 = "SELECT NMB, VAL from " + setting
        cur.execute(line2)
        rows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

def checksetting(setting, value):
    conn = getconn()
    cur = conn.cursor()
    line0 = "SELECT * FROM " + setting + " FETCH FIRST ROW ONLY;"
    cur.execute(line0)
    a = str(cur.fetchone())
    if a.rstrip() != 'None':
        b = a[1:-1].split(', ')[1]
        c = b[1:-1]
        leng = len(c)
        v = ''
        for i in range(leng):
            if i < len(str(value)):
                v += str(value)[i]
            else:
                v += ' '
        line1 = "SELECT NMB FROM "+setting+" WHERE VAL = \'"+v+"\'"
        cur.execute(line1)
        a = str(cur.fetchone())
        if a.rstrip() != 'None':
            x = True
        else:
            x = False
    else:
        x = False
    cur.close()
    conn.close()
    return x


def randomquote():
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT MAX(NUM) FROM inter;")
    r = str(cur.fetchone())
    rr = int(r[1:-2])
    dd = random.randrange(rr + 1)
    cur.execute("SELECT QUOT FROM inter WHERE NUM = %s", ([dd]))
    resp = str(cur.fetchone())
    response = resp[2:-3].strip()
    cur.execute("SELECT TRAN FROM inter WHERE NUM = %s", ([dd]))
    resp1 = str(cur.fetchone())
    response = response + ' - ' + resp1[2:-3].strip()
    cur.execute("SELECT LANG FROM inter WHERE NUM = %s", ([dd]))
    resp2 = str(cur.fetchone())
    response = response + ' - ' + resp2[2:-3].strip()
    cur.close()
    conn.close()
    return response

def addquote(language, line, trans=""):
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT MAX(NUM) FROM inter;")
    a = str(cur.fetchone())
    if a == '(None,)':
        ar = 0
    else:
        ar = int(a[1:-2]) + 1
    cur.execute("INSERT INTO inter VALUES (%s,%s,%s,%s) ON CONFLICT (QUOT) DO NOTHING ;", (ar, language, line, trans))
    conn.commit()
    cur.execute("SELECT NUM, QUOT, TRAN from inter")
    rows = cur.fetchall()
    x = 0
    for j in rows:
        x+=1
    cur.close()
    conn.close()
    return "we have "+str(x) +" quotes so far"

def removelast():
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT MAX(NUM) FROM inter;")
    a = int(str(cur.fetchone())[1:-2])
    cur.execute("DELETE FROM inter WHERE NUM = %s;", ([a]))
    conn.commit()
    cur.execute("SELECT NUM, QUOT, TRAN from inter")
    rows = cur.fetchall()
    x = 0
    for j in rows:
        x+=1
    cur.close()
    conn.close()
    return "we have " + str(x) + " quotes so far"

def quotenum():
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT NUM, QUOT, TRAN from inter")
    rows = cur.fetchall()
    x = 0
    for j in rows:
        x += 1
    cur.close()
    conn.close()
    return "we have " + str(x) + " quotes so far"



def setdefaults():
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM settingspref FETCH FIRST ROW ONLY;")
    a = str(cur.fetchone())
    if a == 'None':
        cur.execute("INSERT INTO settingspref VALUES (0,'/')")
    conn.commit()
    cur.close()
    conn.close()

def setprefix(val):
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM settingspref FETCH FIRST ROW ONLY;")
    a = str(cur.fetchone())
    if a == 'None':
        cur.execute("INSERT INTO settingspref VALUES (0,%s)",(val, ))
    else:
        cur.execute("UPDATE settingspref SET VAL = %s WHERE NMB = 0",(val, ))
    conn.commit()
    cur.close()
    conn.close()

def getprefix():
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT VAL FROM settingspref FETCH FIRST ROW ONLY;")
    a = str(cur.fetchone())
    b = a[2:-3].rstrip()
    cur.close()
    conn.close()
    return b

def getchannel(name):
    conn = getconn()
    cur = conn.cursor()
    line1 = "SELECT VAL FROM " + name
    cur.execute(line1)
    a = str(cur.fetchone())
    b = a.strip(" ,()\'")
    cur.close()
    conn.close()
    return int(b)








