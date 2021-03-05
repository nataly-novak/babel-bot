from dbwork import getconn
import random

def makelore():
    conn = getconn()
    cur = conn.cursor()

    print('koai')

    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('lore',))
    check = (cur.fetchone()[0])
    if not check:
        cur.execute('''CREATE TABLE lore (
        NUM INT  NOT NULL,
        ACTION TEXT NOT NULL,
        LANG TEXT NOT NULL,
        QUOT TEXT  NOT NULL,
        TRAN TEXT
        );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE lore ADD CONSTRAINT test_pkey10 PRIMARY KEY (ACTION, QUOT);')
    else:
        print('No need')
    conn.commit()
    cur.close()
    conn.close()


def filllore():
    conn = getconn()
    cur = conn.cursor()
    f = open("lore", "r",encoding="utf8")
    f1 = f.readlines()
    cnt = 0
    for i in f1:
        a = i[:-1].split(' - ')
        if len(a) < 4:
            a.append('')
        cur.execute("INSERT INTO lore VALUES (%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT test_pkey10 DO NOTHING ;", (cnt, a[0], a[1], a[2], a[3]))
        cnt += 1
    cur.execute("SELECT NUM, ACTION, LANG, QUOT, TRAN from lore")
    rows = cur.fetchall()
    n = len(f1)
    for i in rows:
        print(i)
    f.close()
    conn.commit()
    cur.close()
    conn.close()

def addlore(action, language, line, trans=""):
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT MAX(NUM) FROM lore;")
    a = str(cur.fetchone())
    if a == '(None,)':
        ar = 0
    else:
        ar = int(a[1:-2]) + 1
    cur.execute("INSERT INTO lore VALUES (%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT test_pkey10 DO NOTHING ;", (ar, action, language, line, trans))
    conn.commit()
    cur.execute("SELECT NUM, QUOT, TRAN from lore")
    rows = cur.fetchall()
    x = 0
    for j in rows:
        x+=1
    cur.close()
    conn.close()
    return "we have "+str(x) +" lore entries so far"

def getlore(action):
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT ACTION, LANG, QUOT, TRAN from lore")
    b = cur.fetchall()
    print("______________________\n FETCHED\n")

    a = []
    for i in b:
        if i[0] == action:
            a.append([i[1], i[2], i[3]])
    num = len(a)
    if a == []:
        response = ""
    else:
        i = random.randrange(num)
        line = a[i]
        if line[2]=="":
            response = "`"+line[1]+"`\n"
        else:
            response ="`"+ line[1]+ "("+line[0]+", "+line[2]+")`\n"
    print(response)
    cur.close()
    conn.close()
    return response