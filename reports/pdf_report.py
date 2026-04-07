import pdfkit

def generate_pdf():
    path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

    config = pdfkit.configuration(wkhtmltopdf=path)

    pdfkit.from_file(
        "report.html",
        "report.pdf",
        configuration=config
    )

    print("[+] PDF report saved to report.pdf")