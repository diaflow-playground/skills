#!/usr/bin/env python3
"""
Fetch a Diaflow workflow and save it to a JSON file.

Workflows can be very large (10MB+), so this script writes the response
to a file instead of dumping to the console.

Usage:
    python fetch_workflow.py <uniqueId_or_numericId> [output_path]

    - If output_path is omitted, writes to /tmp/diaflow_<uniqueId>.json
    - Prints only the output file path on success

Requires:
    DIAFLOW_TOKEN environment variable to be set

Exit code: 0 on success, 1 on error
"""

import json
import os
import subprocess
import sys

API_BASE = "https://api.diaflow.io/api/v1"


def fetch_workflow(builder_id, output_path=None):
    token = os.environ.get("DIAFLOW_TOKEN")
    if not token:
        print("Error: DIAFLOW_TOKEN environment variable is not set", file=sys.stderr)
        sys.exit(1)

    url = f"{API_BASE}/builders/{builder_id}"

    result = subprocess.run(
        ["curl", "-s", "-f", url, "-H", f"Authorization: Bearer {token}"],
        capture_output=True,
    )

    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        print(f"Error: curl failed (exit {result.returncode}) — {stderr}", file=sys.stderr)
        sys.exit(1)

    # Parse to extract identifiers and pretty-print
    try:
        workflow = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("Error: Response is not valid JSON", file=sys.stderr)
        sys.exit(1)

    unique_id = workflow.get("uniqueId", builder_id)

    if output_path is None:
        output_path = f"/tmp/diaflow_{unique_id}.json"

    with open(output_path, "w") as f:
        json.dump(workflow, f, indent=2)

    # Print only the path
    print(output_path)


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_workflow.py <uniqueId_or_numericId> [output_path]", file=sys.stderr)
        sys.exit(1)

    builder_id = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    fetch_workflow(builder_id, output_path)


if __name__ == "__main__":
    main()
