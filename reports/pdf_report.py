import pdfkit
import subprocess

def generate_pdf():
    pdfkit.from_file(
        "report.html",
        "report.pdf",
        options={"enable-local-file-access": ""}
    )

    print("[+] PDF report saved to report.pdf")


def generate_pdf(input_html, output_pdf):
    try:
        subprocess.run(
            ["wkhtmltopdf", input_html, output_pdf],
            check=True
        )
        print(f"[+] PDF report saved to {output_pdf}")
    except Exception as e:
        print(f"[!] Error generating PDF: {e}")