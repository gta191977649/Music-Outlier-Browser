import sqlite3

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def executeSQL(sql):
    conn = sqlite3.connect("../db.sqlite3")
    c = conn.cursor()
    c.execute(sql)
    return dictfetchall(c)

def getDataFromArtist(artist):
    return executeSQL("SELECT * from `song_v2` WHERE `artist` = \"{}\"".format(artist))
