#!/usr/bin/python3

from controller import Controller
from model import Model
from GUI import Icon, WinNewEntry, WinList

from PyQt5.QtWidgets import QApplication
import sys

controller = Controller()
model = Model("db", controller)
app = QApplication(sys.argv)
ListWindow = WinList(controller)
NewEntryWindow = WinNewEntry(controller)
icon = Icon(app, NewEntryWindow, ListWindow)
sys.exit(app.exec_())
