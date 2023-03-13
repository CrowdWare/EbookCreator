#############################################################################
# Copyright (C) 2023 CrowdWare
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
from pathlib import Path
from markdown2 import markdown
from tempfile import mkdtemp
from generator import addLineNumbers
from jinja2 import Template
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtGui import QPageLayout, QPageSize
from PySide6.QtWidgets import QApplication, QFileDialog 
from PySide6.QtCore import Qt, QUrl


class HtmlExport():
    def __init__(self, book, status_bar):
        self.status_bar = status_bar
        self.install_directory = os.getcwd()

        filename = ""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("HTML (*.html);;All (*)")
        dialog.setWindowTitle("Create HTML")
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDirectory(book.source_path)
        dialog.setDefaultSuffix("html")
        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
        del dialog
        if not filename:
            return
        
        QApplication.setOverrideCursor(Qt.WaitCursor)
        html = '<?xml version="1.0" encoding="utf-8"?>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">\n'
        html += '<head>\n'
        html += '<link href="file:///' + book.source_path + "/css/pastie.css" + '" rel="stylesheet" type="text/css"/>\n'
        html += '<link href="file:///' + book.source_path + "/css/stylesheet.css" + '\" rel="stylesheet" type="text/css"/>\n'
        html += '<style>@media print {.pagebreak {clear: both;page-break-after: always;}}</style>\n'
        html += '</head>\n<body>\n'
        htm = ""
        if book.theme == "Paperback":
            html += generatePBParts(book)
        else:
            toc, htm, html = generateParts(book, html)
            html += generateToc(book, toc)
            
        html += htm
        html += '\n</body>\n</html>'

        with open(filename, "w") as f:
            f.write(html)
        QApplication.restoreOverrideCursor()
        self.status_bar.showMessage("Ready")

def generatePBParts(book):
    html = ""
    for part in book._parts:
        with open(os.path.join(book.source_path, "parts", part.src), "r") as i:
            text = i.read()
            htm = fixTables(markdown(text, html4tags = False, extras=["fenced-code-blocks", "wiki-tables", "tables", "header-ids"]))
            if book.linenumbers == "True":
                htm = addLineNumbers(htm)
            htm = htm.replace("../images", "file:///" + book.source_path + "/images")
            html += htm
            html += '<div class="pagebreak"></div>\n'
    return html

def generateParts(book, xhtml):
    toc = []

    partNo = 1
    html = ""
    for part in book._parts:
        with open(os.path.join(book.source_path, "parts", part.src), "r") as i:
            text = i.read()
        name = part.name.replace(" ", "-").lower()
        if name == "toc":
            toc_item = {}
            toc_item["href"] = "toc.xhtml"
            if book.language == "de":
                toc_item["name"] = "Inhaltsverzeichnis"
            else:
                toc_item["name"] = "Table of Contents"
            toc_item["id"] = "nav"
            toc_item["parts"] = []
            toc.append(toc_item)
        else:
            htm = fixTables(markdown(text, html4tags = False, extras=["fenced-code-blocks", "wiki-tables", "tables", "header-ids"]))
            list = getLinks(htm, name)
            for item in list:
                toc.append(item)
            # we don't want linenumbers in HTML, which will be converted to PDF 
            if book.linenumbers == "True":
                htm = addLineNumbers(htm)
            # fix img tags
            htm = htm.replace("../images", "file:///" + book.source_path + "/images")
            if partNo < len(book._parts):
                htm += "<p style=\"page-break-before: always\">"
            # should be true for cover page
            if part.pdfOnly:
                xhtml += htm
            else:
                html += htm
        partNo += 1
        
    return toc, html, xhtml

def fixTables(text):
    text = text.replace("<th align=\"center\"", "<th class=\"center\"")
    text = text.replace("<th align=\"right\"", "<th class=\"right\"")
    text = text.replace("<th align=\"left\"", "<th class=\"left\"")
    text = text.replace("<td align=\"center\"", "<td class=\"center\"")
    text = text.replace("<td align=\"right\"", "<td class=\"right\"")
    text = text.replace("<td align=\"left\"", "<td class=\"left\"")
    return text

def getLinks(text, part_name):
    nodes = []
    list = []
    for line in text.split("\n"):
        if not line:
            continue
        if line.startswith("<h1 "):
            c = 1
        elif line.startswith("<h2 "):
            c = 2
        elif line.startswith("<h3 "):
            c = 3
        elif line.startswith("<h4 "):
            c = 4
        elif line.startswith("<h5 "):
            c = 5
        elif line.startswith("<h6 "):
            c = 6
        else:
            c = 0
        if c > 0:
            start = line.find("id=")
            end = line.find('"', start + 4)
            id = line[start + 4:end]

            start = line.find(">", end) + 1
            end = line.find("<", start + 1)
            name = line[start:end]
            item = {}
            item["href"] = "#" + id
            item["name"] = name
            item["id"] = id
            item["parts"] = []
            if len(nodes) < c:
                nodes.append(item)
            else:
                nodes[c - 1] = item
            if c == 1:
                list.append(item)
            else:
                nodes[c - 2]["parts"].append(item)
    return list

def generateToc(book, parts):
    path = os.getcwd()
    context = {}
    context["parts"] = parts
    with open(os.path.join(path, "themes", book.theme, "layout", "toc_pdf.xhtml"), "r") as fp:
        data = fp.read()
    tmp = Template(data)
    xhtml = tmp.render(context)
    return xhtml + '<p style="page-break-before: always">'
