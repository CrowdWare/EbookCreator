import sys
from weasyprint import HTML, CSS

def export(input, output):
    with open(input, "r", encoding="utf-8") as f:
        html = f.read()

    h = HTML(string=html)
    css = CSS(string='@page { size: A5; margin: 0.7cm;}')
    h.write_pdf(output, stylesheets=[css])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python export.py <input.html> <output.pdf>")
        sys.exit()

    export(sys.argv[1], sys.argv[2])