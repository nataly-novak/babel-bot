import psycopg2
from languages import getlanchan

def maketimetable(conn):
    cur = conn.cursor()
    print('timetable')
    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('timetable',))
    check = (cur.fetchone()[0])
    print(check)
    if not check:
        cur.execute('''CREATE TABLE timetable (
                    NMB INT NOT NULL,
                    DAY DATE NOT NULL,
                    CLOCK TIME NOT NULL,
                    CHAN CHAR(30) NOT NULL,
                    NAME CHAR(100) NOT NULL 
                    
                    );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE timetable ADD CONSTRAINT date_key PRIMARY KEY (DAY, CLOCK, CHAN);')
    else:
        print('No need')
    conn.commit()

def addevent(conn, day, clock, chan, name):
        cur = conn.cursor()
        cur.execute("SELECT MAX(NMB) FROM timetable;")
        a = str(cur.fetchone())
        if a == '(None,)':
            ar = 0
        else:
            ar = int(a[1:-2]) + 1
        line = "INSERT INTO timetable VALUES ("+str(ar)+",\'"+day+"\',\'"+clock+"\',\'"+chan+"\',"+"\'"+name+"\')"
        cur.execute(line)
        conn.commit()
        cur.execute("SELECT NMB,DAY, CLOCK, CHAN, NAME from timetable")
        rows = cur.fetchall()
        x = 0
        for j in rows:
            x += 1
            print(j)

def geteventlist(conn):
    eventlist = []
    cur = conn.cursor()
    cur.execute("SELECT NMB,DAY, CLOCK, CHAN, NAME from timetable")
    rows = cur.fetchall()
    for i in rows:
        a = []
        for j in i:
            a.append(j)

        a[3] = getlanchan(conn, a[3].strip('\' '))
        a[4] = a[4].strip('\' ')
        print(a)
        eventlist.append(a)
    return eventlist






