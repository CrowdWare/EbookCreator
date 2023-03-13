from weasyprint import HTML, CSS

filename = "out.pdf"
cssPath = "themes/Epub3DE/assets/css"

html = '<?xml version="1.0" encoding="utf-8"?>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">\n'
html += '<head>\n'
html += "<link href=\"file:///E:/SourceCode/EbookCreator/css/pastie.css rel=\"stylesheet\" type=\"text/css\"/>\n"
html += "<link href=\"file:///E:/SourceCode/EbookCreator/stylesheet.css rel=\"stylesheet\" type=\"text/css\"/>\n"
html += '</head>\n<body>\n'

#toc, htm, html = generateParts(book, html)
#html += generateToc(book, toc)

html += '<p style="page-break-before: always">'
html += "<h1>Title</h1>\n"
html += "<p>Lore, ipsum dolor</p>\n"
html += '\n</body>\n</html>'

h = HTML(string=html)
css = CSS(string='@page { size: A5; margin: 0cm;}')
h.write_pdf(filename, stylesheets=[css])