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

import sys
import os
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtCore import Qt, QCoreApplication, QSettings, QByteArray, QUrl
from PySide6.QtGui import QIcon, QKeySequence, QFont, QPalette, QColor
from PySide6.QtQml import qmlRegisterType
from mainwindow import MainWindow
from ebook import Ebook
from part import Part
import main_rc


if __name__ == "__main__":
    sys.argv.append("--disable-web-security")

    app = QApplication(sys.argv)
    QCoreApplication.setOrganizationName("CrowdWare")
    QCoreApplication.setApplicationName("EbookCreator")
    QCoreApplication.setApplicationVersion("1.5.0")

    app.setStyle(QStyleFactory.create("Fusion"))

    qmlRegisterType(Ebook, 'EbookCreator', 1, 0, 'Ebook')
    qmlRegisterType(Part, 'EbookCreator', 1, 0, 'Part')

    font = QFont("Sans Serif", 10)
    app.setFont(font)
    app.setWindowIcon(QIcon(":/images/logo.svg"))

    win = MainWindow(app)
    win.show()
    sys.exit(app.exec())
