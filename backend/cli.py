import argparse
import requests
import os

API_URL = "http://127.0.0.1:5000/debug"


def read_code_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(
        description="Offline Competitive Programming Debugger"
    )

    parser.add_argument(
        "file",
        help="Path to C++ source file"
    )

    parser.add_argument(
        "--fix",
        action="store_true",
        help="Generate corrected code"
    )

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print("Error: File not found")
        return

    code = read_code_file(args.file)

    payload = {
        "code": code,
        "fix": args.fix
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code != 200:
            print("\nBackend Error")
            return

        data = response.json()
        analysis = data.get("analysis", "No output received")

        mode = "FIX MODE" if args.fix else "ANALYSIS MODE"

        print(f"\n[{mode}]\n")
        print(analysis)

    except Exception as e:
        print(f"\nConnection Error: {e}")

if __name__ == "__main__":
    main()