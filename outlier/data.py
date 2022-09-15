import sqlite3
from unittest import result

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def executeSQL(sql,params = None):
    conn = sqlite3.connect("../db.sqlite3")
    c = conn.cursor()
    if params: c.execute(sql,params)
    else: c.execute(sql)
    return dictfetchall(c)

def getDataFromArtist(artist):
    return executeSQL("SELECT * from `song_v2` WHERE `artist` = ?",(artist,))

def getAllArtistList(min=None):
    sql = "SELECT artist ,COUNT(*) as songs from `song_v2` GROUP BY `artist` HAVING COUNT(*) > {}".format(min) \
        if min != None else "SELECT `artist` from `song_v2` GROUP BY `artist`"
    row = executeSQL(sql)
    results = []
    for item in row:
        results.append(item["artist"])
    return results
    