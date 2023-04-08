import pdfkit

html_file = "output.html"
pdf_file = "output.pdf"

options = {
    "page-size": "A4",
    "dpi": 300,
    "disable-smart-shrinking": "",
    "quiet": ""
}

pdfkit.from_file(html_file, pdf_file, options=options)
