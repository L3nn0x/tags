#!/usr/bin/python3

import sqlite3

class   Entry:
    def __init__(self, (data, date, tags)):
        self.data = data
        self.date = date
        self.tags = tags

class   Bdd:
    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect(filename)
        c = self.conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL UNIQUE, date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);")
        c.execute("CREATE TABLE IF NOT EXISTS tags(id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT NOT NULL UNIQUE);")
        c.execute("CREATE TABLE IF NOT EXISTS links(id INTEGER PRIMARY KEY AUTOINCREMENT, dataID INTEGER NOT NULL, tagID INTEGER NOT NULL, FOREIGN KEY(dataID) REFERENCES data(id), FOREIGN KEY(tagID) REFERENCES tags(id));")

    def __del__(self):
        self.save()

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
                result.append(Entry((i[0][0], i[0][1], i[1])))
        return result

    def findTags(self, partial):
        c = self.conn.cursor()
        c.execute("SELECT tag FROM tags WHERE tag like '%{}%';".format(partial))
        data = c.fetchall()
        if data == None:
            return []
        return [i[0] for i in data]

    def findData(self, data = None):
        c = self.conn.cursor()
        if data != None:
            c.execute("SELECT data.data, data.date, tags.tag FROM data INNER JOIN links ON data.id == links.dataID INNER JOIN tags ON links.tagID == tags.id WHERE data.data like ?;", (data,))
        else:
            c.execute("SELECT data.data, data.date, tags.tag FROM data INNER JOIN links ON data.id == links.dataID INNER JOIN tags ON links.tagID == tags.id;")
        return [Entry(i) for i in c.fetchall()]

    def deleteData(self, data):
        c = self.conn.cursor()
        c.execute("SELECT links.tagID FROM data INNER JOIN links ON data.id=links.dataID WHERE data.data like ?;", (data,))
        tagsToCheck = [i[0] for i in c.fetchall()]
        c.execute("SELECT id FROM data WHERE data like ?;", (data,))
        idData = c.fetchone()
        if idData != None:
            idData = idData[0]
            c.execute("DELETE FROM data WHERE id=?;", (idData,))
            c.execute("DELETE FROM links WHERE dataID=?;", (idData,))
        for i in tagsToCheck:
            c.execute("SELECT COUNT(*) FROM links WHERE tagID=?;", (i,))
            if c.fetchone()[0] <= 1:
                c.execute("DELETE FROM tags WHERE id=?;", (i,))

    def deleteTagFromData(self, data, tag):
        c = self.conn.cursor()
        c.execute("DELETE links FROM links INNER JOIN data ON links.dataID=data.id INNER JOIN tags ON links.tagID=tags.id WHERE data.data like ? && tags.tag like ?;", (data, tag))

    def save(self):
        self.conn.commit()

def test(a):
    a.addEntry("test", ("fun", "cool"))
    a.addEntry("test2", ("sexy", "fun"))
    a.addEntry("test3", "cool")
    a.addEntry("test4", ("fun", "sexy", "cool"))
    a.addEntry("test5", ("core", "fury", "saxo"))
