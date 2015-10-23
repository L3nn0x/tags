#!/usr/bin/python3

from bdd import Bdd

from controller import *

class   Model:
    def __init__(self, dbname, eventManager):
        self.bdd = Bdd(dbname)
        self.manager = eventManager
        self.manager.addObserver(self)

    def notify(self, e):
        if type(e) is NewDataEvent:
            self.bdd.addEntry(e.data, e.tags)
            self.manager.notify(UpdateListEvent(self.bdd.findData(e.data)[0], True))
        elif type(e) is GetAllEvent:
            for i in self.bdd.findData():
                self.manager.notify(UpdateListEvent(i, True))
        elif type(e) is SearchEvent:
            r = self.bdd.getTagFilter(e.s)
            if len(r) == 0:
                tags = self.bdd.findTags(e.s)
                r = []
                for i in tags:
                    for j in self.bdd.getTagFilter(i):
                        r.append(j)
            for i in r:
                self.manager.notify(UpdateListEvent(i, True))