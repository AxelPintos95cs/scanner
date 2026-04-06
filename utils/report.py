import json
from datetime import datetime

def save_json(findings, filename="report.json"):
    report = {
        "timestamp": datetime.now().isoformat(),
        "findings": findings
    }

    with open(filename, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[+] Report saved to {filename}")