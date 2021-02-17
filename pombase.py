from pommer import Pommer
from raid import Raid
emojis = {"🗡":"sword", "🛡️":"defence", "💊":"heal", "⛏":"axe", "💣":"fire","❓":"debuff"}

def makepombases(conn):
    cur = conn.cursor()
    print('pombase')
    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('pombase',))
    check = (cur.fetchone()[0])
    print(check)
    if not check:
        cur.execute('''CREATE TABLE pombase(
                    NMB INT NOT NULL,
                    STAMP TIMESTAMP NOT NULL,
                    AMNT INT NOT NULL,
                    MMBR CHAR(200) NOT NULL,
                    ACTS CHAR(200) NOT NULL,
                    TRIGGERED INT NOT NULL,
                    ATTACKS CHAR(200) NOT NULL,
                    BHP INT NOT NULL,
                    VHP INT NOT NULL,
                    BAB INT NOT NULL,
                    AC INT NOT NULL,
                    SAVE INT NOT NULL, 
                    DAMAGE INT NOT NULL 

                    );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE pombase ADD CONSTRAINT pom_key PRIMARY KEY (NMB);')
    else:
        print('No need')
    conn.commit()
    print('pommers')
    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('pommers',))
    check = (cur.fetchone()[0])
    print(check)
    if not check:
        cur.execute('''CREATE TABLE pommers (
                    NMB INT NOT NULL,
                    POMMER CHAR(50) NOT NULL,
                    HP INT NOT NULL,              
                    AC INT NOT NULL,
                    DAMAGE INT NOT NULL,
                    ATTACK INT NOT NULL,
                    TOTAL INT NOT NULL,
                    POMS CHAR(400),
                    STAGGERED INT  NOT NULL 
                    );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE pommers ADD CONSTRAINT pommer_key PRIMARY KEY (POMMER);')
    else:
        print('No need')
    conn.commit()
    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('isgame',))
    check = (cur.fetchone()[0])
    print(check)
    if not check:
        cur.execute('''CREATE TABLE isgame(
                    NMB INT NOT NULL,
                    VAL BOOLEAN NOT NULL
                    );''')
        print("Table created successfully")
    else:
        print('No need')
    conn.commit()
    cur.execute("INSERT INTO isgame VALUES (0,%s)", ("FALSE",))
    conn.commit()



def setgame(conn, val):
    cur = conn.cursor()
    cur.execute("SELECT * FROM isgame FETCH FIRST ROW ONLY;")
    a = str(cur.fetchone())
    if a == 'None':
        cur.execute("INSERT INTO isgame VALUES (0,%s)", (val,))
    else:
        cur.execute("UPDATE isgame SET VAL = %s WHERE NMB = 0", (val,))
    conn.commit()

def checkgame(conn):
    cur = conn.cursor()
    cur.execute("SELECT VAL FROM isgame FETCH FIRST ROW ONLY;")
    a = (cur.fetchone())
    b = a[0]
    return b

def getuserval(conn, user):
    cur = conn.cursor()
    cur.execute("SELECT POMMER, HP, AC, DAMAGE, ATTACK, TOTAL, POMS, STAGGERED FROM pommers WHERE POMMER = %s", (str(user).ljust(50),))
    resp = (cur.fetchone())
    if resp == None:
        return None
    else:
        for i in resp:
            print(i)
        return Pommer(resp[0].rstrip(),resp[1],resp[2],resp[3], resp[4], resp[5], resp[6].rstrip(), resp[7])



def setuserval(conn, pommer: Pommer):
    cur = conn.cursor()
    print("-"+str(pommer.user).ljust(50)+"-")
    cur.execute("SELECT POMMER FROM pommers WHERE POMMER = %s", (str(pommer.user).ljust(50),))
    resp = (cur.fetchone())

    print(resp)
    cur.execute("SELECT MAX(NMB) FROM pommers;")
    r = str(cur.fetchone())
    print(r)
    if r[1:-2] != 'None':
        rr = int(r[1:-2])+1
    else:
        rr = 0

    if resp != None:
        isNew = False
    else:
        isNew = True
    print(isNew)
    if isNew:
        cur.execute("INSERT INTO pommers VALUES (%s,%s,%s,%s, %s,%s,%s,%s, %s)", (str(rr), str(pommer.user), str(pommer.hp), str(pommer.ac), str(pommer.damage), str(pommer.attack), str(pommer.total), str(pommer.poms), str(pommer.staggered)))
    else:
        cur.execute("UPDATE pommers SET HP= %s, AC=%s,  DAMAGE=%s, ATTACK=%s, TOTAL=%s, POMS=%s, STAGGERED = %s WHERE POMMER = %s", (str(pommer.hp), str(pommer.ac), str(pommer.damage), str(pommer.attack), str(pommer.total), str(pommer.poms), str(pommer.staggered), str(pommer.user)))
    conn.commit()


def getraidstat(conn):
    cur = conn.cursor()
    cur.execute("SELECT MAX(NMB) FROM pombase;")
    a = str(cur.fetchone())
    if a == '(None,)':
        ar = -1
    else:
        ar = int(a[1:-2])
    if ar == -1:
        return Raid("",0,"")
    else:
        cur.execute("SELECT STAMP, AMNT, MMBR,ACTS,TRIGGERED, ATTACKS, BHP, VHP, BAB, AC, SAVE, DAMAGE  FROM pombase WHERE NMB = %s",(ar,))
        resp = (cur.fetchone())
        for i in resp:
            print(i)
        return Raid(str(resp[0]), resp[1], resp[2].rstrip(), resp[3].rstrip(), resp[4], resp[5].rstrip, resp[6], resp[7], resp[8], resp[9], resp[10], resp[11] )



def setraidstat(conn, raid: Raid):
    cur = conn.cursor()
    cur.execute("SELECT MAX(NMB) FROM pombase;")
    a = str(cur.fetchone())
    if a == '(None,)':
        ar = 0
    else:
        ar = int(a[1:-2]) + 1
    cur.execute("INSERT INTO pombase VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)",(str(ar), str(raid.stamp),str(raid.amnt),str(raid.mmbr),str(raid.acts), str(raid.trg), str(raid.attacks), str(raid.bhp), str(raid.vhp),str(raid.bab), str(raid.ac), str(raid.save), str(raid.damage) ) )
    conn.commit()

def getaction(emoji):
    return emojis[emoji]