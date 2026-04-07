import html


def generate_html(findings, filename="report.html"):
    grouped = {"HIGH": [], "MEDIUM": [], "LOW": []}
    header_urls = []

    for f in findings:
        if f["type"] == "Missing Security Headers":
            header_urls.append(f["url"])
        else:
            grouped[f["severity"]].append(f)

    total = len(findings)
    high = len(grouped["HIGH"])
    medium = len(grouped["MEDIUM"]) + (1 if header_urls else 0)
    low = len(grouped["LOW"])

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

    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Security Scan Report</title>

        <style>
            body {{
                font-family: Arial;
                padding: 20px;
                background: #f5f5f5;
            }}

            h1 {{
                color: #222;
            }}

            h2 {{
                margin-top: 40px;
                border-bottom: 2px solid #ddd;
                padding-bottom: 5px;
            }}

            .summary {{
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }}

            .box {{
                padding: 10px 15px;
                border-radius: 6px;
                color: white;
                font-weight: bold;
            }}

            .high {{ background: #e74c3c; }}
            .medium {{ background: #f39c12; }}
            .low {{ background: #27ae60; }}
            .total {{ background: #34495e; }}

            .card {{
                background: white;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            }}

            .card h3 {{
                margin-top: 0;
            }}

            code {{
                background: #eee;
                padding: 8px;
                border-radius: 6px;
                display: block;
                margin-top: 8px;
                overflow-x: auto;
            }}

            a {{
                color: #3498db;
                text-decoration: none;
            }}

            a:hover {{
                text-decoration: underline;
            }}

            ul {{
                max-height: 200px;
                overflow-y: auto;
                background: #fafafa;
                padding: 10px;
                border-radius: 6px;
            }}
        </style>
    </head>

    <body>
        <h1>🔐 Security Scan Report</h1>

        <!-- SUMMARY -->
        <div class="summary">
            <div class="box high">HIGH: {high}</div>
            <div class="box medium">MEDIUM: {medium}</div>
            <div class="box low">LOW: {low}</div>
            <div class="box total">TOTAL: {total}</div>
        </div>
    """

    for severity, items in grouped.items():
        if not items:
            continue

        html_content += f"<h2 class='{severity.lower()}'>{severity}</h2>"

        for f in items:
            poc_block = ""
            if "poc" in f:
                poc_block = f"""
                <p><strong>PoC:</strong></p>
                <code>{html.escape(f['poc'])}</code>
                <a href="{f['poc']}" target="_blank">🔗 Test exploit</a>
                """

            html_content += f"""
            <div class="card">
                <h3>{f['type']} <span class="box {severity.lower()}">{severity}</span></h3>

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
        unique_urls = sorted(set(header_urls))

        html_content += f"""
        <h2 class="medium">MEDIUM</h2>
        <div class="card">
            <h3>Missing Security Headers</h3>

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