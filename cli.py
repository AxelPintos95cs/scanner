import argparse
from core.scanner import run_scan
from utils.report import save_json
from reports.html_report import generate_html

def main():
    parser = argparse.ArgumentParser(description="Mini Web Vulnerability Scanner")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--depth", type=int, default=2)

    args = parser.parse_args()

    results: list = run_scan(args.url, args.depth)

    print("\n=== RESULTS ===")
    save_json(results)
    generate_html(results)

    for r in results:
        print(f"[{r['severity']}] {r['type']} at {r['url']}")
        if "details" in r:
            print(f"  -> {r['details']}")

if __name__ == "__main__":
    main()

