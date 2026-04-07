import html


def generate_html(findings, filename="report.html"):
    grouped = {"HIGH": [], "MEDIUM": [], "LOW": []}
    header_urls = []

    for f in findings:
        if f["type"] == "Missing Security Headers":
            header_urls.append(f["url"])
        else:
            grouped[f["severity"]].append(f)

    description = {
        "XSS": "User input is reflected without sanitization.",
        "SQL Injection": "Database queries may be manipulated.",
        "Missing Security Headers": "Important security headers are not set."
    }

    impact = {
        "XSS": "An attacker can execute malicious scripts in the user's browser.",
        "SQL Injection": "An attacker can manipulate database queries and access sensitive data.",
        "Missing Security Headers": "The application is more vulnerable to common web attacks."
    }

    recommendation = {
        "XSS": "Sanitize and validate all user inputs.",
        "SQL Injection": "Use parameterized queries and ORM frameworks.",
        "Missing Security Headers": "Implement headers like CSP, HSTS, and X-Frame-Options."
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
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
                padding: 30px;
                background: #f4f6f9;
                color: #333;
            }}

            h1 {{
                margin-bottom: 20px;
            }}

            h2 {{
                margin-top: 40px;
                border-bottom: 2px solid #ddd;
                padding-bottom: 5px;
            }}

            .summary {{
                display: flex;
                gap: 15px;
                margin-bottom: 30px;
            }}

            .box {{
                flex: 1;
                padding: 20px;
                border-radius: 10px;
                color: white;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }}

            .high {{ background: #e74c3c; }}
            .medium {{ background: #f39c12; }}
            .low {{ background: #27ae60; }}
            .total {{ background: #34495e; }}

            .card {{
                background: white;
                border-left: 6px solid #ccc;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.05);
                transition: transform 0.1s ease;
            }}

            .card:hover {{
                transform: translateY(-2px);
            }}

            .card.high {{ border-color: #e74c3c; }}
            .card.medium {{ border-color: #f39c12; }}
            .card.low {{ border-color: #27ae60; }}

            .badge {{
                display: inline-block;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                color: white;
                margin-left: 10px;
            }}

            .badge.high {{ background: #e74c3c; }}
            .badge.medium {{ background: #f39c12; }}
            .badge.low {{ background: #27ae60; }}

            code {{
                background: #eee;
                padding: 10px;
                border-radius: 6px;
                display: block;
                margin-top: 10px;
                overflow-x: auto;
            }}

            a {{
                color: #3498db;
                text-decoration: none;
                word-break: break-all;
            }}

            a:hover {{
                text-decoration: underline;
            }}

            ul {{
                max-height: 250px;
                overflow-y: auto;
                background: #fafafa;
                padding: 10px;
                border-radius: 6px;
            }}

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
    """

    for severity, items in grouped.items():
        if not items:
            continue

        html_content += f"<h2>{severity}</h2>"

        for f in items:
            poc_block = ""
            if "poc" in f:
                poc_block = f"""
                <p><strong>PoC:</strong></p>
                <code>{html.escape(f['poc'])}</code>
                <a href="{f['poc']}" target="_blank">🔗 Test exploit</a>
                """

            html_content += f"""
            <div class="card {severity.lower()}">
                <h3>
                    {f['type']}
                    <span class="badge {severity.lower()}">{severity}</span>
                </h3>

                <p><strong>URL:</strong>
                    <a href="{f['url']}" target="_blank">{f['url']}</a>
                </p>

                <p><strong>Description:</strong> {description.get(f['type'], '')}</p>
                <p><strong>Impact:</strong> {impact.get(f['type'], '')}</p>
                <p><strong>Recommendation:</strong> {recommendation.get(f['type'], '')}</p>

                {poc_block}
            </div>
            """

    if header_urls:
        unique_urls = list(set(header_urls))

        html_content += f"""
        <h2>MEDIUM</h2>
        <div class="card medium">
            <h3>
                Missing Security Headers
                <span class="badge medium">MEDIUM</span>
            </h3>

            <p><strong>Description:</strong> {description['Missing Security Headers']}</p>
            <p><strong>Impact:</strong> {impact['Missing Security Headers']}</p>
            <p><strong>Recommendation:</strong> {recommendation['Missing Security Headers']}</p>

            <p><strong>Affected URLs ({len(unique_urls)}):</strong></p>
            <ul>
        """

        for url in unique_urls:
            html_content += f'<li><a href="{url}" target="_blank">{url}</a></li>'

        html_content += "</ul></div>"

    html_content += "</body></html>"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] HTML report saved to {filename}")