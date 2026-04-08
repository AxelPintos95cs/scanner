import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request
import asyncio

from core.scanner import run_scan

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = None

    if request.method == "POST":
        url = request.form.get("url")
        depth = int(request.form.get("depth", 2))
        print("Entró a index")

        if request.method == "POST":
            print("POST recibido")

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

            except Exception as e:
                print(f"[ERROR] {e}")

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)