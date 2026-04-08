# filepath: pdf_report.py
import pdfkit
import subprocess

def generate_pdf():
    # Esta función no se usa, puedes eliminarla si quieres
    pdfkit.from_file(
        "report.html",
        "report.pdf",
        options={"enable-local-file-access": ""}
    )
    print("[+] PDF report saved to report.pdf")

def generate_pdf(input_html, output_pdf):
    try:
        # Especifica el path completo a wkhtmltopdf.exe
        wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # Ajusta si la ruta es diferente
        subprocess.run(
            [wkhtmltopdf_path, input_html, output_pdf],
            check=True
        )
        print(f"[+] PDF report saved to {output_pdf}")
    except Exception as e:
        print(f"[!] Error generating PDF: {e}")