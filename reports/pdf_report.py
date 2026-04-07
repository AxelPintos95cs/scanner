import pdfkit

def generate_pdf():
    pdfkit.from_file(
        "report.html",
        "report.pdf",
        options={"enable-local-file-access": ""}
    )

    print("[+] PDF report saved to report.pdf")