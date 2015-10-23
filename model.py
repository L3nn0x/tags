#!/usr/bin/python3

from bdd import Bdd
from controller import *

def sortByDate(l):
    import operator
    return sorted(l, key=operator.attrgetter('date'), reverse=True)
    

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
            r = sortByDate(self.bdd.findData())
            for i in r:
                self.manager.notify(UpdateListEvent(i, True))
        elif type(e) is SearchEvent:
            r = self.bdd.getTagFilter(e.s)
            tags = self.bdd.findTags(e.s)   # Recherche les tags suggérés et les ajoute aux tags exacts trouvés
            for i in tags:
                for j in self.bdd.getTagFilter(i):
                    if not j in r:
                        r.append(j)
            r = sortByDate(r)
            for i in r:
                self.manager.notify(UpdateListEvent(i, True))
