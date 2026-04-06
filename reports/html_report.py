def generate_html(findings, filename="report.html"):
    html = """
    <html>
    <head>
        <title>Security Scan Report</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            .high { color: red; }
            .medium { color: orange; }
            .card {
                border: 1px solid #ddd;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <h1>Security Scan Report</h1>
    """

    for f in findings:
        severity = f["severity"].lower()

        description = {
            "XSS": "User input is reflected without sanitization.",
            "SQL Injection": "Database queries may be manipulated.",
            "Missing Security Headers": "Important security headers are not set."
        }.get(f["type"], "")

        html += f"""
        <div class="card {severity}">
            <h3>{f['type']} ({f['severity']})</h3>
            <p><strong>URL:</strong> {f['url']}</p>
            <p><strong>Description:</strong> {description}</p>
        </div>
        """

    html += "</body></html>"

    with open(filename, "w") as f:
        f.write(html)

    print(f"[+] HTML report saved to {filename}")