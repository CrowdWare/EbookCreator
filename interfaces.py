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

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

class GeneratorInterface(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.class_name = ""
        self.display_name = ""
        self.version = ""
        self.text_edit = None

    def setTextEdit(self, te):
        self.text_edit = te

    def menu_action(self):
        pass