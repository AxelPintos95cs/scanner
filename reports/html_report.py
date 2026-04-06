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

    html = """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Security Scan Report</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f5f5f5; }
            h1 { color: #333; }
            h2 { margin-top: 30px; }
            .high { color: red; }
            .medium { color: orange; }
            .low { color: green; }
            .card {
                background: white;
                border: 1px solid #ddd;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            ul { margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>Security Scan Report</h1>
    """

    for severity, items in grouped.items():
        if not items:
            continue

        html += f"<h2 class='{severity.lower()}'>{severity}</h2>"

        for f in items:
            html += f"""
            <div class="card {severity.lower()}">
                <h3>{f['type']}</h3>
                <p><strong>URL:</strong> {f['url']}</p>
                <p><strong>Description:</strong> {description.get(f['type'], '')}</p>
                <p><strong>Impact:</strong> {impact.get(f['type'], '')}</p>
                <p><strong>Recommendation:</strong> {recommendation.get(f['type'], '')}</p>
            </div>
            """

    if header_urls:
        unique_urls = list(set(header_urls))

        html += f"""
        <h2 class="medium">MEDIUM</h2>
        <div class="card medium">
            <h3>Missing Security Headers</h3>
            <p><strong>Description:</strong> {description['Missing Security Headers']}</p>
            <p><strong>Impact:</strong> {impact['Missing Security Headers']}</p>
            <p><strong>Recommendation:</strong> {recommendation['Missing Security Headers']}</p>
            <p><strong>Affected URLs ({len(unique_urls)}):</strong></p>
            <ul>
        """

        for url in unique_urls:
            html += f"<li>{url}</li>"

        html += "</ul></div>"

    html += "</body></html>"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[+] HTML report saved to {filename}")