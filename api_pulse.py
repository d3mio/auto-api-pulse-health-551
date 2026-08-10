"""
ApiPulse — Lightweight Async HTTP Endpoint Health Guard
Usage:
    python api_pulse.py --urls https://httpbin.org/status/200
"""

import time
import argparse
import requests

def check_endpoints(urls: list[str]):
    print(f"[ApiPulse] Monitoring {len(urls)} target endpoints...")
    print("=" * 60)
    for url in urls:
        start = time.time()
        try:
            resp = requests.get(url, timeout=5)
            latency_ms = round((time.time() - start) * 1000, 2)
            status_code = resp.status_code
            status_str = "[OK]" if status_code < 400 else "[FAIL]"
            print(f"{status_str} {url:<45} | Status: {status_code} | Latency: {latency_ms}ms")
        except Exception as e:
            print(f"[ERR] {url:<45} | Error: {e}")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ApiPulse Health Guard")
    parser.add_argument("--urls", nargs="+", default=["https://httpbin.org/status/200"], help="List of URLs")
    args = parser.parse_args()
    check_endpoints(args.urls)
