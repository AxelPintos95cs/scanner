def generate_html(findings, filename="report.html"):
    html = """
    <html>
    <head>
        <title>Scan Report</title>
        <style>
            body { font-family: Arial; }
            .high { color: red; }
            .medium { color: orange; }
        </style>
    </head>
    <body>
        <h1>Vulnerability Report</h1>
        <ul>
    """

    for f in findings:
        severity_class = f["severity"].lower()
        html += f"""
        <li class="{severity_class}">
            <strong>{f['type']}</strong> - {f['url']}
        </li>
        """

    html += """
        </ul>
    </body>
    </html>
    """

    with open(filename, "w") as f:
        f.write(html)

    print(f"[+] HTML report saved to {filename}")