import sqlite3


def put(discord_id, stepartist, database):
    db = sqlite3.connect(database)
    cur = db.cursor()
    data = (discord_id, stepartist)
    try:
        cur.execute(f"SELECT discord_id FROM stepartists WHERE discord_id ={discord_id}")
    except sqlite3.OperationalError:
        init(db)
    result = cur.fetchone()
    if result:
        print(f"User {stepartist} already in database! Skipping...")
        db.close()
    else:
        cur.execute("INSERT INTO stepartists VALUES(?, ?)", data)
        db.commit()
        print("Values added to db:")
        print(cur.execute("SELECT * from stepartists").fetchall()[-1])
        db.close()


def get(database):
    db = sqlite3.connect(database)
    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM stepartists")
    except sqlite3.OperationalError:
        init(db)
    fetched = cur.fetchall()
    print(type(fetched))
    db.close()
    return fetched

def wipe(database):
    db = sqlite3.connect(database)
    try:
        db.execute("DELETE FROM stepartists")
    except sqlite3.OperationalError:
        init(db)
    db.commit()
    db.close()
    print("DB should be wiped! Make sure to check though...")


def init(db):
    db.execute("CREATE TABLE IF NOT EXISTS stepartists (discord_id INT, stepartist_name TEXT)")