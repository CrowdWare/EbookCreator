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
from PySide6.QtCore import QObject, Property, QFileInfo, ClassInfo
from PySide6.QtQml import ListProperty
from part import Part

@ClassInfo(DefaultProperty = 'parts')
class Ebook(QObject):

    def __init__(self, parent = None):
        super().__init__(parent)
        self._name = ""
        self._theme = ""
        self._language = ""
        self._creator = ""
        self._publisher = ""
        self._size = ""
        self._linenumbers = "True"
        self._parts = []
        self.filename = ""
        self.source_path = ""
        self.window = ""

    def item(self, n):
        return self._parts[n]

    def itemCount(self):
        return len(self._parts)

    def appendItem(self, item):
        self._parts.append(item)

    parts = ListProperty(Part, appendItem)

    @Property('QString')
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @Property('QString')
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        self._language = language

    @Property('QString')
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, theme):
        self._theme = theme

    @Property('QString')
    def creator(self):
        return self._creator

    @creator.setter
    def creator(self, creator):
        self._creator = creator

    @Property('QString')
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, publisher):
        self._publisher = publisher

    @Property('QString')
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @Property("QString")
    def linenumbers(self):
        return self._linenumbers
    
    @linenumbers.setter
    def linenumbers(self, value):
        self._linenumbers = value

    def setFilename(self, filename):
        info = QFileInfo(filename)
        self.filename = info.fileName()
        self.source_path = info.path()

    def setWindow(self, window):
        self.window = window

    def getPart(self, name):
        for part in self._parts:
            if part.name == name or part.src == name.lower() + ".md":
                return part
        return None

    def dropPart(self, partname):
        part = self.getPart(partname)
        filename = os.path.join(self.source_path, "parts", part.src)
        os.remove(filename)
        self._parts.remove(part)
        self.save()

    def addPart(self, name):
        part = Part()
        part.name = name
        part.src = name.replace(" ", "").lower() + ".md"
        self._parts.append(part)
        with open(os.path.join(self.source_path, "parts", part.src), "w", encoding='utf-8') as f:
            f.write("")
        self.save()

    def updatePart(self, oldname, newname):
        part = self.getPart(oldname)
        part.name = newname
        self.save()

    def partUp(self, partname):
        part = self.getPart(partname)
        pos = self._parts.index(part)
        self._parts.remove(part)
        self._parts.insert(pos - 1, part)
        self.save()

    def partDown(self, partname):
        part = self.getPart(partname)
        pos = self._parts.index(part)
        self._parts.remove(part)
        self._parts.insert(pos + 1, part)
        self.save()

    def save(self):
        fname = os.path.join(self.source_path, self.filename)
        with open(fname, "w", encoding='utf-8') as f:
            f.write("import EbookCreator 1.0\n\n")
            f.write("Ebook {\n")
            f.write("    name: \"" + self._name + "\"\n")
            f.write("    language: \"" + self._language + "\"\n")
            f.write("    size: \"" + self._size + "\"\n")
            f.write("    linenumbers: \"" + self._linenumbers + "\"\n")
            f.write("    theme: \"" + self._theme + "\"\n")
            f.write("    creator: \"" + self._creator + "\"\n")
            for part in self._parts:
                f.write("    Part {\n")
                f.write("        src: \"" + part.src + "\"\n")
                f.write("        name: \"" + part.name + "\"\n")
                if part.pdfOnly:
                    f.write("        pdfOnly: true\n")
                f.write("    }\n")
            f.write("}\n")
