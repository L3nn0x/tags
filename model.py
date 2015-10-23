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
            for i in self.bdd.getTagFilter(e.s):
                self.manager.notify(UpdateListEvent(i, True))