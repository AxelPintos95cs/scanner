import tempfile
import sys
import os
import time
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request, send_file
from reports.pdf_report import generate_pdf
import asyncio

from core.scanner import run_scan

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    results = None

    if request.method == "POST":
        url = request.form.get("url")
        depth = int(request.form.get("depth", 2))

        print("[WEB] POST recibido")

        if url:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                results = loop.run_until_complete(run_scan(url, depth))

                loop.close()

                if results:
                    severity_order = {"high": 0, "medium": 1, "low": 2}
                    results = sorted(
                        results,
                        key=lambda item: severity_order.get(
                            str(item.get("severity", "")).lower(), 3
                        ),
                    )

                app.config["LAST_RESULTS"] = results

            except Exception as e:
                print(f"[ERROR] {e}")

    return render_template("index.html", results=results)


@app.route("/download_pdf")
def download_pdf():
    try:
        if "LAST_RESULTS" not in app.config or not app.config["LAST_RESULTS"]:
            return "No results to generate report", 400

        results = app.config["LAST_RESULTS"]

        temp_dir = tempfile.gettempdir()
        timestamp = int(time.time())

        html_path = os.path.join(temp_dir, f"web_report_{timestamp}.html")
        pdf_path = os.path.join(temp_dir, f"web_report_{timestamp}.pdf")

        print("[PDF] Rendering index.html in PDF mode...")

        # 🔥 CLAVE: pdf_mode=True
        rendered_html = render_template(
            "index.html",
            results=results,
            pdf_mode=True,
            now=datetime.now().strftime("%Y-%m-%d %H:%M")
        )

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)

        print("[PDF] Generating PDF...")
        generate_pdf(html_path, pdf_path)

        if not os.path.exists(pdf_path):
            return "Error generating PDF", 500

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="scan_report.pdf"
        )

    except Exception as e:
        print(f"[ERROR PDF] {e}")
        return "Error generating PDF", 500


if __name__ == "__main__":
    app.run(debug=True)