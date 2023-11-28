import sqlite3


def put(discord_id, stepartist):
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    data = (discord_id, stepartist)
    cur.execute(f"SELECT discord_id FROM stepartists WHERE discord_id ={discord_id}")
    result = cur.fetchone()
    if result:
        print("User already in database! Skipping...")
        db.close()
    else:
        cur.execute("INSERT INTO stepartists VALUES(?, ?)", data)
        db.commit()
        print("Values added to db:")
        print(cur.execute("SELECT * from stepartists").fetchall()[-1])
        db.close()


def get():
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM stepartists")
    fetched = cur.fetchall()
    print(type(fetched))
    db.close()
    return fetched
