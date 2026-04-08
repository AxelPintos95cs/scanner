import html


def generate_html(findings, filename="report.html"):
    grouped = {"HIGH": [], "MEDIUM": [], "LOW": []}
    header_urls = []

    for f in findings:
        sev = f.get("severity", "").upper()
        if sev in grouped:
            grouped[sev].append(f)

    description = {
        "XSS": "User input is reflected without sanitization.",
        "SQL Injection": "Database queries may be manipulated.",
        "Missing Security Headers": "Important security headers are not set."
    }

    impact = {
        "XSS": "An attacker can execute malicious scripts in the user's browser.",
        "SQL Injection": "An attacker can manipulate database queries.",
        "Missing Security Headers": "Application is vulnerable to common attacks."
    }

    recommendation = {
        "XSS": "Sanitize and validate inputs.",
        "SQL Injection": "Use parameterized queries.",
        "Missing Security Headers": "Implement CSP, HSTS, etc."
    }

    total = len(findings)
    high = len(grouped["HIGH"])
    medium = len(grouped["MEDIUM"]) + (1 if header_urls else 0)
    low = len(grouped["LOW"])

    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Security Scan Report</title>

        <style>
            body {{
                font-family: -apple-system, Segoe UI, Roboto;
                padding: 30px;
                background: #f4f6f9;
            }}

            h1 {{ margin-bottom: 20px; }}

            .summary {{
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }}

            .box {{
                flex: 1;
                padding: 15px;
                border-radius: 8px;
                color: white;
                text-align: center;
                font-weight: bold;
            }}

            .high {{ background: #e74c3c; }}
            .medium {{ background: #f39c12; }}
            .low {{ background: #27ae60; }}
            .total {{ background: #34495e; }}

            .controls {{
                margin-bottom: 20px;
            }}

            input {{
                padding: 8px;
                width: 250px;
                border-radius: 6px;
                border: 1px solid #ccc;
            }}

            button {{
                padding: 8px 12px;
                margin-left: 5px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }}

            .card {{
                background: white;
                border-left: 5px solid #ccc;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
            }}

            .card.high {{ border-color: #e74c3c; }}
            .card.medium {{ border-color: #f39c12; }}
            .card.low {{ border-color: #27ae60; }}

            .badge {{
                padding: 3px 8px;
                border-radius: 5px;
                color: white;
                font-size: 12px;
                margin-left: 10px;
            }}

            .badge.high {{ background: #e74c3c; }}
            .badge.medium {{ background: #f39c12; }}
            .badge.low {{ background: #27ae60; }}

            code {{
                background: #eee;
                padding: 6px;
                display: block;
                margin-top: 5px;
                overflow-x: auto;
            }}

            a {{ color: #3498db; }}
        </style>
    </head>

    <body>

    <h1>🔐 Security Scan Report</h1>

    <div class="summary">
        <div class="box high">HIGH<br>{high}</div>
        <div class="box medium">MEDIUM<br>{medium}</div>
        <div class="box low">LOW<br>{low}</div>
        <div class="box total">TOTAL<br>{total}</div>
    </div>

    <div class="controls">
        <input type="text" id="search" placeholder="Search URL or type...">
        <button onclick="filterSeverity('ALL')">All</button>
        <button onclick="filterSeverity('HIGH')">HIGH</button>
        <button onclick="filterSeverity('MEDIUM')">MEDIUM</button>
        <button onclick="filterSeverity('LOW')">LOW</button>
    </div>
    """

    for severity, items in grouped.items():
        for f in items:
            poc_block = ""
            if "poc" in f:
                poc_block = f"""
                <code>{html.escape(f['poc'])}</code>
                <a href="{f['poc']}" target="_blank">🔗 Test</a>
                """

            html_content += f"""
            <div class="card {severity.lower()}"
                 data-severity="{severity}"
                 data-url="{f['url']}"
                 data-type="{f['type']}">

                <h3>{f['type']}
                    <span class="badge {severity.lower()}">{severity}</span>
                </h3>

                <p><a href="{f['url']}" target="_blank">{f['url']}</a></p>
                <p>{description.get(f['type'], '')}</p>
                <p><strong>Impact:</strong> {impact.get(f['type'], '')}</p>
                <p><strong>Fix:</strong> {recommendation.get(f['type'], '')}</p>

                {poc_block}
            </div>
            """

    if header_urls:
        unique_urls = list(set(header_urls))

        for url in unique_urls:
            html_content += f"""
            <div class="card medium"
                 data-severity="MEDIUM"
                 data-url="{url}"
                 data-type="Missing Security Headers">

                <h3>Missing Security Headers
                    <span class="badge medium">MEDIUM</span>
                </h3>

                <p><a href="{url}" target="_blank">{url}</a></p>
            </div>
            """

    html_content += """
    <script>
        const searchInput = document.getElementById("search");

        searchInput.addEventListener("input", function() {
            const value = this.value.toLowerCase();
            const cards = document.querySelectorAll(".card");

            cards.forEach(card => {
                const url = card.dataset.url.toLowerCase();
                const type = card.dataset.type.toLowerCase();

                if (url.includes(value) || type.includes(value)) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });

        function filterSeverity(level) {
            const cards = document.querySelectorAll(".card");

            cards.forEach(card => {
                if (level === "ALL") {
                    card.style.display = "block";
                } else {
                    card.style.display =
                        card.dataset.severity === level ? "block" : "none";
                }
            });
        }
    </script>
    """

    html_content += "</body></html>"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] HTML report saved to {filename}")