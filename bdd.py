#!/usr/bin/python3

import sqlite3

class   Bdd:
    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect(filename)
        c = self.conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL UNIQUE, date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);")
        c.execute("CREATE TABLE IF NOT EXISTS tags(id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT NOT NULL UNIQUE);")
        c.execute("CREATE TABLE IF NOT EXISTS links(id INTEGER PRIMARY KEY AUTOINCREMENT, dataID INTEGER NOT NULL, tagID INTEGER NOT NULL, FOREIGN KEY(dataID) REFERENCES data(id), FOREIGN KEY(tagID) REFERENCES tags(id));")

    def __del__(self):
        self.conn.commit()

    def addEntry(self, data, tags):
        if type(tags) != list and type(tags) != tuple:
            tags = [tags]
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO data(data) values(?);", (data,))
        except sqlite3.IntegrityError:
            pass
        c.execute("SELECT id FROM data WHERE data like ?;", (data,));
        idData = c.fetchone()[0]
        idTags = []
        for tag in tags:
            try:
                c.execute("INSERT INTO tags(tag) values(?);", (tag,))
            except sqlite3.IntegrityError:
                pass
            c.execute("SELECT id FROM tags WHERE tag like ?", (tag,))
            idTags.append(c.fetchone()[0])
        for i in idTags:
            c.execute("INSERT INTO links(dataID, tagID) VALUES(?, ?);", (idData, i))

    def getTagFilter(self, tags):
        if type(tags) != list and type(tags) != tuple:
            tags = [tags]
        c = self.conn.cursor()
        c.execute("SELECT DISTINCT data.data, data.date, tags.tag FROM data INNER JOIN links ON data.id == links.dataID INNER JOIN tags ON links.tagID == tags.id WHERE tags.tag IN ({});".format("'" + "','".join(tags) + "'"))
        data = c.fetchall()
        from collections import defaultdict
        table = defaultdict(set)
        for i in data:
            table[(i[0], i[1])].add(i[2])
        result = []
        tags = set(tags)
        for i in table.items():
            if i[1] == tags:
                result.append(i[0])
        return result

    def findTags(self, partial):
        c = self.conn.cursor()
        c.execute("SELECT tag FROM tags WHERE tag like '%{}%';".format(partial))
        return [i[0] for i in c.fetchall()]

def test(a):
    a.addEntry("test", ("fun", "cool"))
    a.addEntry("test2", ("sexy", "fun"))
    a.addEntry("test3", "cool")
    a.addEntry("test4", ("fun", "sexy", "cool"))
    a.addEntry("test5", ("core", "fury", "saxo"))
