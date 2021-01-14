import psycopg2

def maketimetable(conn):
    cur = conn.cursor()
    print('timetable')
    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('timetable',))
    check = (cur.fetchone()[0])
    print(check)
    if not check:
        cur.execute('''CREATE TABLE languages (
                    NMB INT NOT NULL,
                    DAY DATE NOT NULL,
                    CLOCK TIME NOT NULL,
                    CHAN CHAR(30) NOT NULL,
                    NAME CHAR(100) NOT NULL 
                    
                    );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE languages ADD CONSTRAINT date_key PRIMARY KEY (DAY, CLOCK, CHAN);')
    else:
        print('No need')
    conn.commit()

def addevent(conn, day, clock, chan, name)
        cur = conn.cursor()
        cur.execute("SELECT MAX(NMB) FROM timetable;")
        a = str(cur.fetchone())
        if a == '(None,)':
            ar = 0
        else:
            ar = int(a[1:-2]) + 1
        line = "INSERT INTO timetable VALUES ("+str(ar)+","+day+","+clock+",\""+chan+"\","+"\""+name+"\")"
        print(line)
        conn.commit()
        cur.execute("SELECT NMB,DAY, CLOCK, CHAN, NAME from languages")
        rows = cur.fetchall()
        x = 0
        for j in rows:
            x += 1
            print(j)
