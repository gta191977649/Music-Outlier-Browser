import sqlite3
import outlier.config as CONF
import pathlib
import seaborn as sns
import numpy as np

from unittest import result

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def executeSQL(sql, params=None):
    #path = "{}/{}".format(pathlib.Path().resolve(), CONF.DB_PATH)
    conn = sqlite3.connect(CONF.DB_PATH)
    c = conn.cursor()
    if params:
        c.execute(sql, params)
    else:
        c.execute(sql)
    return dictfetchall(c)


def getDataFromArtist(artist):
    return executeSQL("SELECT * from `song_v2` WHERE `artist` = ?", (artist,))

def getDataFromGenre(genre):
    return executeSQL("SELECT * from `song_v2` WHERE `genre` LIKE ?", (genre,))

def getSongsByGenre(genre):
    data = getDataFromGenre(genre)
    print(data)
def getArtistsByGenre(genre,limit=None):
    if limit:
        artists = executeSQL("SELECT * from `song_v2` WHERE `genre` LIKE ? GROUP BY artist LIMIT ?", (genre,limit))
    else:
        artists = executeSQL("SELECT * from `song_v2` WHERE `genre` LIKE ? GROUP BY artist", (genre,))
    x = np.array(list(map(lambda x: x['artist'], artists)))
    return x
def getAllArtistList(min=None):
    sql = "SELECT artist ,COUNT(*) as songs from `song_v2` GROUP BY `artist` HAVING COUNT(*) > {}".format(min) \
        if min != None else "SELECT `artist` from `song_v2` GROUP BY `artist`"
    row = executeSQL(sql)
    results = []
    for item in row:
        results.append(item["artist"])
    return results

def getDataFromArtistByFeatureDiscriminator(artist, discriminator="tempo", filterNoise=False):
    data = getDataFromArtist(artist)
    if not data: raise ("Invaild artist")
    x = []
    if filterNoise:
        for v in data:
            if v[discriminator] > 0:
                x.append(v[discriminator])
    else:
        x = np.array(list(map(lambda x: x[discriminator], data)))
    return np.array(x)
