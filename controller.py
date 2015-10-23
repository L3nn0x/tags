#!/usr/bin/python3

from weakref import WeakKeyDictionary

class   Event:
    def __init__(self):
        self.name = "general event"

    def __str__(self):
        return self.name

class   NewDataEvent(Event):
    def __init__(self, data, tags):
        self.name = "new data event"
        self.data = data
        self.tags = tags

class   UpdateListEvent(Event):
    def __init__(self, entry, add):
        self.name = "update event"
        self.add = add
        self.data = entry.data
        self.tags = entry.tags
        self.date = entry.date
        
class SearchEvent(Event):
    def __init__(self, s):
        self.name = "search event"
        self.s = s

class   GetAllEvent(Event):
    def __init__(self):
        self.name = "get all event"

class   Controller:
    def __init__(self):
        self.observers = WeakKeyDictionary()

    def addObserver(self, observer):
        self.observers[observer] = 1

    def delObserver(self, observer):
        try:
            del self.observers[observer]
        except KeyError:
            pass

    def notify(self, event):
        for key in self.observers:
            key.notify(event)
