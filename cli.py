import argparse
from core.scanner import run_scan

def main():
    parser = argparse.ArgumentParser(description="Mini Web Vulnerability Scanner")
    parser.add_argument("--url", required=True, help="Target URL")

    args = parser.parse_args()

    results = run_scan(args.url)

    print("\n=== RESULTS ===")

    for r in results:
        print(f"[{r['severity']}] {r['type']} at {r['url']}")
        if "details" in r:
            print(f"  -> {r['details']}")

if __name__ == "__main__":
    main()