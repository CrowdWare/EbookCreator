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
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import QParallelAnimationGroup, QPropertyAnimation, Qt, Property, Signal, QDir, QFile, QIODevice
from PySide6.QtGui import QImage, QPalette, QPixmap, QColor, QIcon
import resources


class Expander(QWidget):
    expanded = Signal(object)
    clicked = Signal()

    def __init__(self, header, svg):
        QWidget.__init__(self)
        self.svg = svg
        self.is_expanded = False
        self.text = header
        self.icon = QLabel()
        self.hyper = QLabel()
        self.setColors()
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover, True)
        self.setAutoFillBackground(True)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        hbox.addWidget(self.icon)
        hbox.addSpacing(5)
        hbox.addWidget(self.hyper)
        hbox.addStretch()
        hbox.setContentsMargins(4, 4, 4, 4)
        vbox.addLayout(hbox)
        self.content = QWidget()
        self.content.setStyleSheet("background-color: " + self.palette().base().color().name())
        self.content.setMaximumHeight(0)
        vbox.addWidget(self.content)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)
        self.hyper.linkActivated.connect(self.buttonClicked)

        self.anim = QParallelAnimationGroup()
        self.height_anim = QPropertyAnimation(self.content, "maximumHeight".encode("utf-8"))
        self.color_anim = QPropertyAnimation(self, "color".encode("utf-8"))
        self.height_anim.setDuration(200)
        self.color_anim.setDuration(200)
        self.anim.addAnimation(self.height_anim)
        self.anim.addAnimation(self.color_anim)

    def setColors(self):
        self.label_normal_color = self.palette().link().color().name()
        self.label_hovered_color = self.palette().highlight().color().name()
        self.label_selected_color = self.palette().highlightedText().color().name()
        self.normal_color = self.palette().base().color().name()
        self.selected_color = self.palette().highlight().color()
        self.hovered_color = self.palette().alternateBase().color()

        self.normal_icon = QPixmap(self.createIcon(self.svg, self.normal_color))
        self.hovered_icon = QPixmap(self.createIcon(self.svg, self.label_hovered_color))
        self.selected_icon = QPixmap(self.createIcon(self.svg, self.label_hovered_color))

        self.icon.setPixmap(self.normal_icon)
        self.color = self.normal_color

        self.hyper.setText("<a style=\"color: " + self.label_normal_color + " text-decoration: none\" href=\"#\">" + self.text + "</a>")

    def createIcon(self, source, hilite_color):
        temp = QDir.tempPath()
        file = QFile(source)
        file.open(QIODevice.ReadOnly | QIODevice.Text)
        data = str(file.readAll(), encoding="utf-8")
        file.close()

        out = os.path.join(temp, hilite_color + ".svg")
        with open(out, "w", encoding='utf-8') as fp:
            fp.write(data.replace("#ff00ff", hilite_color))
        return out

    def setExpanded(self, value):
        if value == self.is_expanded:
            return

        if value:
            self.is_expanded = True
            pal = self.palette()
            pal.setColor(QPalette.Window, self.selected_color)
            self.setPalette(pal)
            self.icon.setPixmap(self.selected_icon)
            self.hyper.setText("<a style=\"color: " + self.label_selected_color + "; text-decoration: none;\" href=\"#\">" + self.text + "</a>")
        else:
            self.is_expanded = False
            pal = self.palette()
            pal.setColor(QPalette.Window, QColor(self.normal_color))
            self.setPalette(pal)
            self.icon.setPixmap(self.normal_icon)
            self.hyper.setText("<a style=\"color: " + self.label_normal_color + "; text-decoration: none;\" href=\"#\">" + self.text + "</a>")

        if self.is_expanded:
            self.expandContent()
        else:
            self.collapseContent()
        self.expanded.emit(self.is_expanded)

    def addLayout(self, layout):
        self.content.setLayout(layout)

    @Property('QColor')
    def color(self):
        return Qt.black

    @color.setter
    def color(self, color):
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(color))
        self.setPalette(pal)

    def mouseReleaseEvent(self, me):
        if me.button() != Qt.LeftButton or me.y() > 32:
            return
        self.setExpanded(not self.is_expanded)
        if self.is_expanded:
            self.clicked.emit()

    def expandContent(self):
        if self.content.layout():
            self.height_anim.setEndValue(self.content.layout().sizeHint().height())
        else:
            self.height_anim.setEndValue(0)
        self.height_anim.setStartValue(0)
        self.color_anim.setStartValue(self.normal_color)
        self.color_anim.setEndValue(self.selected_color)
        self.anim.start()

    def collapseContent(self):
        if self.content.layout():
            self.height_anim.setStartValue(self.content.layout().sizeHint().height())
        else:
            self.height_anim.setStartValue(0)
        self.height_anim.setEndValue(0)
        self.color_anim.setStartValue(self.selected_color)
        self.color_anim.setEndValue(self.normal_color)
        self.anim.start()

    def buttonClicked(self):
        self.setExpanded(not self.is_expanded)
        if self.is_expanded:
            self.clicked.emit()

    def enterEvent(self, event):
        if not self.is_expanded:
            pal = self.palette()
            pal.setColor(QPalette.Window, QColor(self.hovered_color))
            self.setPalette(pal)
            self.icon.setPixmap(self.hovered_icon)
            self.hyper.setText("<a style=\"color: " + self.label_hovered_color + "; text-decoration: none;\" href=\"#\">" + self.text + "</a>")
        QWidget.enterEvent(self, event)

    def leaveEvent(self, event):
        if not self.is_expanded:
            pal = self.palette()
            pal.setColor(QPalette.Window, QColor(self.normal_color))
            self.setPalette(pal)
            self.icon.setPixmap(self.normal_icon)
            self.hyper.setText("<a style=\"color: " + self.label_normal_color + "; text-decoration: none;\" href=\"#\">" + self.text + "</a>")
        QWidget.leaveEvent(self, event)
