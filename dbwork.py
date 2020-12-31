import os
import psycopg2

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