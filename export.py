from weasyprint import HTML, CSS

with open("E:/SourceCode/PySide6DesktopBookEnglishPaperback/pythongui.html", "r", encoding="utf-8") as f:
    html = f.read()

h = HTML(string=html)
css = CSS(string='@page { size: A5; margin: 0.7cm;}')
h.write_pdf("E:/SourceCode/PySide6DesktopBookEnglishPaperback/pythongui.pdf", stylesheets=[css])
