import os
import psycopg2
import random

def settingsdb(conn):
    cur = conn.cursor()
    print('settingsdb')
    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('settingspins',))
    check = (cur.fetchone()[0])
    print(check)
    if not check:
        cur.execute('''CREATE TABLE settingspins (
            NMB INT NOT NULL,
            VAL CHAR(20) NOT NULL
            );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE settingspins ADD CONSTRAINT test_pkey2 PRIMARY KEY (VAL);')
    else:
        print('No need')
        conn.commit()


def makedb(conn):
    cur = conn.cursor()

    print('koai')

    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('inter',))
    check = (cur.fetchone()[0])
    print(check)
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

def filldb(conn):
    cur = conn.cursor()
    f = open("international", "r")
    f1 = f.readlines()
    cnt = 0
    for i in f1:
        a = i[:-1].split(' - ')
        if len(a) < 3:
            a.append('')
        cur.execute("INSERT INTO inter VALUES (%s,%s,%s,%s) ON CONFLICT (QUOT) DO NOTHING ;", (cnt, a[0], a[1], a[2]))
        cnt += 1
        print(cnt)
    cur.execute("SELECT NUM, LANG, QUOT, TRAN from inter")
    rows = cur.fetchall()
    for j in rows:
        print(j)
    n = len(f1)
    print(n)
    f.close()

def addsetting(conn, setting, value):
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
    print(line1)
    conn.commit()

    cur.execute(line1)
    line2 = "SELECT NMB, VAL from "+setting
    cur.execute(line2)
    rows = cur.fetchall()
    for j in rows:
        print(j)


def removesetting(conn, setting, value):
    cur = conn.cursor()
    line0 = "SELECT * FROM "+setting+" FETCH FIRST ROW ONLY;"
    print(line0)
    cur.execute(line0)
    a = str(cur.fetchone())
    b = a[1:-1].split(', ')[1]
    c = b[1:-1]
    print(c)
    if a != '(None,)':
        leng = len(c)
        v = ''
        for i in range(leng):
            if i<len(str(value)):
                v+=str(value)[i]
            else:
                v+=' '
        print(v)
        line1 = "DELETE FROM "+setting+" WHERE VAL = \'"+value+"\'"
        print(line1)
        cur.execute(line1)
        line2 = "SELECT NMB, VAL from " + setting
        cur.execute(line2)
        rows = cur.fetchall()
        for j in rows:
            print(j)
    conn.commit()




def randomquote(conn):
    cur = conn.cursor()
    cur.execute("SELECT MAX(NUM) FROM inter;")
    r = str(cur.fetchone())
    rr = int(r[1:-2])
    print(rr)
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
    print(response)
    return response

def addquote(conn, language, line, trans=""):
    cur = conn.cursor()
    cur.execute("SELECT MAX(NUM) FROM inter;")
    a = str(cur.fetchone())
    print(a)
    if a == '(None,)':
        ar = 0
    else:
        ar = int(a[1:-2]) + 1
    print(ar)
    cur.execute("INSERT INTO inter VALUES (%s,%s,%s,%s) ON CONFLICT (QUOT) DO NOTHING ;", (ar, language, line, trans))
    conn.commit()
    cur.execute("SELECT NUM, QUOT, TRAN from inter")
    rows = cur.fetchall()
    for j in rows:
        print(j)

def removelast(conn):
    cur = conn.cursor()
    cur.execute("SELECT MAX(NUM) FROM inter;")
    a = int(str(cur.fetchone())[1:-2])
    print(a)
    cur.execute("DELETE FROM inter WHERE NUM = %s;", ([a]))
    conn.commit()
    cur.execute("SELECT NUM, QUOT, TRAN from inter")
    rows = cur.fetchall()
    for j in rows:
        print(j)