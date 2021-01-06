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
            NMB CHAR (30) NOT NULL,
            VAL CHAR(100)  NOT NULL
            );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE settingspins ADD CONSTRAINT test_pkey2 PRIMARY KEY (NMB);')
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
    cur.execute("SELECT MAX(NMB) FROM %s;",(setting))
    a = str(cur.fetchone())
    print(a)
    if a == '(None,)':
        ar = 0
    else:
        ar = int(a[1:-2]) + 1

    cur.execute("INSERT INTO %s VALUES (%s,%s)", (setting,ar, value))
    cur.execute("SELECT NMB, VAL from %s",(setting))
    rows = cur.fetchall()
    for j in rows:
        print(j)


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