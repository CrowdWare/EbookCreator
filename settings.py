#############################################################################
# Copyright (C) 2024 CrowdWare
#
# This file is part of EbookCreator.
#
#  EbookCreator is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  EbookCreator is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with EbookCreator.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import os
import shutil
from shutil import rmtree
from PySide6.QtCore import (QCoreApplication, QParallelAnimationGroup,
                          QPropertyAnimation, Qt, Property, Signal)
from PySide6.QtGui import QColor, QImage, QPalette, QPixmap
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QGridLayout, QComboBox, QLineEdit, QPushButton, QCheckBox


class Settings(QDialog):

    def __init__(self, book, install_directory, parent = None):
        super(Settings, self).__init__(parent)
        self.book = book
        self.saved = False
        self.install_directory = install_directory
        self.setWindowTitle(QCoreApplication.applicationName() + " - Book Settings")
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Ok")
        self.ok_button.setDefault(True)
        self.ok_button.setEnabled(False)
        cancel_button = QPushButton("Cancel")
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(cancel_button)
        layout = QGridLayout()
        self.title = QLineEdit()
        self.title.setText(book.name)
        self.title.setMinimumWidth(200)
        self.creator = QLineEdit()
        self.creator.setText(book.creator)
        self.language = QComboBox()
        self.language.setEditable(True)
        self.language.addItem("de")
        self.language.addItem("en")
        self.language.addItem("es")
        self.language.addItem("it")
        self.language.addItem("fr")
        self.language.setEditText(book.language)
        self.theme = QComboBox()

        dir = os.path.join(install_directory, "themes")
        for r, dirs, f in os.walk(dir):
            if r == dir:
                for d in dirs:
                    self.theme.addItem(d)
        self.theme.setCurrentText(book.theme)
        self.linenumbers = QCheckBox()
        if book.linenumbers == "True":
            self.linenumbers.setChecked(True)
        else:
            self.linenumbers.setChecked(False)
        layout.addWidget(QLabel("Title"), 0, 0)
        layout.addWidget(self.title, 0, 1, 1, 3)
        layout.addWidget(QLabel("Creator"), 1, 0)
        layout.addWidget(self.creator, 1, 1, 1, 3)
        layout.addWidget(QLabel("Language"), 2, 0)
        layout.addWidget(self.language, 2, 1)
        layout.addWidget(QLabel("Theme"), 3, 0)
        layout.addWidget(self.theme, 3, 1)
        layout.addWidget(QLabel("Linenumbers"), 4, 0)
        layout.addWidget(self.linenumbers, 4, 1)
        layout.addLayout(button_layout, 5, 0, 1, 4)
        self.setLayout(layout)

        self.ok_button.clicked.connect(self.okClicked)
        cancel_button.clicked.connect(self.cancelClicked)
        self.title.textChanged.connect(self.textChanged)
        self.creator.textChanged.connect(self.textChanged)
        self.language.editTextChanged.connect(self.textChanged)
        self.theme.currentIndexChanged.connect(self.textChanged)
        self.linenumbers.stateChanged.connect(self.textChanged)

    def okClicked(self):
        if self.book.name != self.title.text():
            self.book.name = self.title.text()
        self.book.creator = self.creator.text()
        self.book.language = self.language.currentText()
        if self.linenumbers.isChecked():
            self.book.linenumbers = "True"
        else:
            self.book.linenumbers = "False"
        if self.book.theme != self.theme.currentText:
            self.book.theme = self.theme.currentText()
            #copy theme files
            rmtree(os.path.join(self.book.source_path, "css"))
            shutil.copytree(os.path.join(self.install_directory, "themes", self.book.theme, "assets", "css"), os.path.join(self.book.source_path, "css"))

        self.book.save()
        self.saved = True
        self.close()

    def cancelClicked(self):
        self.close()

    def textChanged(self):
        self.ok_button.setEnabled(True)
