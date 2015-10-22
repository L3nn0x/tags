#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSystemTrayIcon, QMenu, QAction, QLineEdit, QLabel, QTableWidget, QGridLayout, QTableWidgetItem
from PyQt5.QtGui import QIcon
import signal
from controller import *

signal.signal(signal.SIGINT, signal.SIG_DFL)

class WinNewEntry(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.initUI()
        self.controller = controller

    def initUI(self):
        self.setGeometry(200,200,500,200)
        self.setWindowTitle('Tag Indexer: Add an entry')
        
        lblURL = QLabel('URL:', self)

        lblTags = QLabel('Tags:', self)
        lblTags.setToolTip('À séparer par des virgules')

        self.champURL = QLineEdit(self)

        self.champTags = QLineEdit(self) 

        btnEnr = QPushButton('Enregistrer',self)
        btnEnr.clicked.connect(self.save)

        btnAnnul = QPushButton('Annuler',self)
        btnAnnul.clicked.connect(self.hide)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(lblURL, 0,0)
        grid.addWidget(self.champURL, 0, 3, 1, 6)
        grid.addWidget(lblTags, 4, 0)
        grid.addWidget(self.champTags, 4, 3, 1, 6)
        grid.addWidget(btnAnnul, 9, 7)
        grid.addWidget(btnEnr, 9, 8)
        self.setLayout(grid)


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.hide()

    def closeEvent(self, e):
        self.hide()
        e.ignore()

    def save(self):
        print("URL: "+self.champURL.text())
        print("Tags: "+self.champTags.text())
        e = NewDataEvent(self.champURL.text(), self.champTags.text())
        self.champURL.setText('')
        self.champTags.setText('')
        self.hide()
        self.controller.notify(e)

    def cancel(self):
        self.champURL.setText('')
        self.champTags.setText('')
        self.hide()

class WinList(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.initUI()
        self.controller = controller
        self.controller.addObserver(self)
        self.controller.notify(GetAllEvent())

    def initUI(self):
        self.setGeometry(200,200,600,280)
        self.setWindowTitle('Tag Indexer: List')
        
        self.tab = QTableWidget(self)
        self.tab.showGrid = False
        
        self.tab.horizontalHeader().setSectionResizeMode(1)
        self.tab.setColumnCount(3)
    
        lblRecherche = QLabel('Recherche: ', self)

        btnRecherche = QPushButton('Rechercher', self)
        
        self.recherche = QLineEdit()
        

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(lblRecherche, 0,0)
        grid.addWidget(btnRecherche, 0, 8)
        grid.addWidget(self.recherche, 0, 1, 1, 7)
        grid.addWidget(self.tab,4,0, 6,9)

        self.tab.setHorizontalHeaderLabels(('URL','Tags','Date d\'ajout'))
        self.setLayout(grid)

    def addLine(self, url, tags, date):
        l = self.tab.rowCount()
        self.tab.setRowCount(l+1)
        self.tab.setItem(l, 0, QTableWidgetItem(url))
        self.tab.setItem(l, 1, QTableWidgetItem(tags))
        self.tab.setItem(l, 2, QTableWidgetItem(date))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.hide()

    def closeEvent(self, e):
        self.hide()
        e.ignore()

    def notify(self, e):
        if type(e) is UpdateListEvent:
            if e.add:
                self.addLine(e.data, ', '.join(e.tags), e.date)

class Icon(QWidget):
    def __init__(self, app, newEntry, listWin):
        super().__init__()
        self.newEntry = newEntry
        self.listWin = listWin
        self.app = app
        self.initUI()

    def initUI(self):
        
        menu = QMenu()
        Ajouter = QAction(QIcon(''), '&Ajouter un tag', menu)
        Ajouter.triggered.connect(self.newEntry.show)
        menu.addAction(Ajouter)

        ouvrir = QAction(QIcon(''), '&Ouvrir', menu)
        ouvrir.triggered.connect(self.listWin.show)
        menu.addAction(ouvrir)

        Quitter = QAction(QIcon(''), '&Quitter', menu)
        Quitter.triggered.connect(self.app.exit)
        menu.addAction(Quitter)

        self.icon = QSystemTrayIcon()
        self.icon.setIcon(QIcon('./icone.png'))
        self.icon.setContextMenu(menu)
        self.icon.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ListWindow = WinList()
    NewEntryWindow = WinNewEntry()
    #NewEntryWindow.show()
    #ListWindow.show()    
    icon = Icon()
    sys.exit(app.exec_())

