import argparse
import asyncio

from core.scanner import run_scan
from utils.report import save_json
from reports.html_report import generate_html
from utils.http import close  
from reports.pdf_report import generate_pdf

async def main():
    parser = argparse.ArgumentParser(description="Mini Web Vulnerability Scanner")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--depth", type=int, default=2)

    args = parser.parse_args()

    results: list = await run_scan(args.url, args.depth)

    print("\n=== RESULTS ===")
    save_json(results, "output/report.json")
    generate_html(results, "output/report.html")
    generate_pdf("output/report.html", "output/report.pdf")

    for r in results:
        print(f"[{r['severity']}] {r['type']} at {r['url']}")
        if "details" in r:
            print(f"  -> {r['details']}")

    await close()


if __name__ == "__main__":
    asyncio.run(main())