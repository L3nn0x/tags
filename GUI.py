#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import bdd as BDD
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSystemTrayIcon, QMenu, QAction, QLineEdit, QLabel, QTableWidget, QGridLayout, QTableWidgetItem
from PyQt5.QtGui import QIcon
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

class FenetreNewEntry(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200,200,500,200)
        self.setWindowTitle('Tag Indexer: Add an entry')
        
        lblURL = QLabel('URL:', self)

        lblTags = QLabel('Tags:', self)
        lblTags.setToolTip('À séparer par des virgules')

        self.champURL = QLineEdit(self)
        self.champURL.returnPressed.connect(self.enregistrer)

        self.champTags = QLineEdit(self)
        self.champTags.returnPressed.connect(self.enregistrer)

        btnEnr = QPushButton('Enregistrer',self)
        btnEnr.clicked.connect(self.enregistrer)

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

    def enregistrer(self):
        tags = self.champTags.text().split(",")
        for i in range(len(tags)):
            if tags[i][0] == ' ':
                tags[i] = tags[i][1:]
        bdd.addEntry(self.champURL.text(),tags)
        self.champURL.setText('')
        self.champTags.setText('')
        self.hide()

    def annuler(self):
        self.champURL.setText('')
        self.champTags.setText('')
        self.hide()

class FenetreListe(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200,200,600,280)
        self.setWindowTitle('Tag Indexer: List')
        
        self.tab = QTableWidget(self)
        self.tab.showGrid = False
        
        self.tab.horizontalHeader().setSectionResizeMode(1)
        self.tab.setColumnCount(3)
    
        lblRecherche = QLabel('Recherche: ', self)

        btnRecherche = QPushButton('Rechercher', self)
        btnRecherche.clicked.connect(self.rechercher)
        
        self.recherche = QLineEdit()
        self.recherche.returnPressed.connect(self.rechercher)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(lblRecherche, 0,0)
        grid.addWidget(btnRecherche, 0, 8)
        grid.addWidget(self.recherche, 0, 1, 1, 7)
        grid.addWidget(self.tab,4,0, 6,9)

        self.tab.setHorizontalHeaderLabels(('URL','Tags','Date d\'ajout'))
        #self.ajouteLigne("http://pouet.pouet", "tag1, tag2", "10/10/2015")
        
        self.setLayout(grid)

    def ajouteLigne(self, url, tags, date):
        l = self.tab.rowCount()
        self.tab.setRowCount(l+1)
        self.tab.setItem(l, 0, QTableWidgetItem(url))
        self.tab.setItem(l, 1, QTableWidgetItem(tags))
        self.tab.setItem(l, 2, QTableWidgetItem(date))
        
    def vider(self):
        self.tab.setRowCount(0)
        
    def rechercher(self):
        self.vider()
        liste = bdd.getTagFilter(self.recherche.text())
        if liste == []:
            liste = bdd.findTags(self.recherche.text())
        #print(liste)
        for i in liste:
            self.ajouteLigne(i.data,", ".join(i.tags), i.date)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.hide()

    def closeEvent(self, e):
        self.hide()
        e.ignore()

class Icone(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        menu = QMenu()
        Ajouter = QAction(QIcon(''), '&Ajouter un tag', menu)
        Ajouter.triggered.connect(NewEntryWindow.show)
        menu.addAction(Ajouter)

        ouvrir = QAction(QIcon(''), '&Ouvrir', menu)
        ouvrir.triggered.connect(ListWindow.show)
        menu.addAction(ouvrir)

        Quitter = QAction(QIcon(''), '&Quitter', menu)
        Quitter.triggered.connect(app.exit)
        menu.addAction(Quitter)

        self.icon = QSystemTrayIcon()
        self.icon.setIcon(QIcon('./icone.png'))
        self.icon.setContextMenu(menu)
        self.icon.show()


bdd = BDD.Bdd('bdd.db')
app = QApplication(sys.argv)
ListWindow = FenetreListe()
NewEntryWindow = FenetreNewEntry()
#NewEntryWindow.show()
#ListWindow.show()
icon = Icone()

