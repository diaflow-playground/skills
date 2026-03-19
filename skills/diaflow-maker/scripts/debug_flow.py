#!/usr/bin/env python3
"""
Debug a Diaflow chat flow by creating a conversation, sending a message,
and polling for execution results — all via the API, no browser needed.

Usage:
    python debug_flow.py <uniqueId> <message> [--workspace-id WID] [--output PATH] [--timeout SECS] [--verbose]

Examples:
    python debug_flow.py JlFO1d16b9 "Hello, I want to buy a shirt"
    python debug_flow.py JlFO1d16b9 "test" --workspace-id 256 --verbose
    python debug_flow.py JlFO1d16b9 "hi" --output /tmp/debug_result.json --timeout 120

Requires:
    DIAFLOW_TOKEN environment variable
    DIAFLOW_WORKSPACE_ID environment variable (or --workspace-id flag)

The script:
    1. Fetches the builder to get the numeric ID and workspace info
    2. Creates a test conversation
    3. Sends the message to trigger flow execution
    4. Polls process-checks until completion or timeout
    5. Outputs a structured debug report

Exit code: 0 on success (flow completed), 1 on error, 2 on timeout
"""

import argparse
import json
import os
import subprocess
import sys
import time


API_BASE = "https://api.diaflow.io/api/v1"


def api_call(method, path, token, workspace_id=None, body=None):
    """Make an API call and return (status_code, parsed_json)."""
    url = f"{API_BASE}{path}"
    cmd = ["curl", "-s", "-w", "\n%{http_code}", url, "-X", method]
    cmd.extend(["-H", f"Authorization: Bearer {token}"])
    cmd.extend(["-H", "Accept: application/json"])
    if workspace_id:
        cmd.extend(["-H", f"Workspace-Id: {workspace_id}"])
    if body:
        cmd.extend(["-H", "Content-Type: application/json"])
        cmd.extend(["-d", json.dumps(body)])

    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        return None, {"detail": f"curl failed: {result.stderr.decode()[:200]}"}

    output = result.stdout.decode("utf-8", errors="replace")
    lines = output.rsplit("\n", 1)
    if len(lines) == 2:
        body_str, status = lines
    else:
        body_str, status = output, "0"

    try:
        status_code = int(status.strip())
    except ValueError:
        status_code = 0

    try:
        data = json.loads(body_str)
    except json.JSONDecodeError:
        data = {"raw": body_str[:500]}

    return status_code, data


def main():
    parser = argparse.ArgumentParser(description="Debug a Diaflow chat flow via API")
    parser.add_argument("unique_id", help="Builder uniqueId (e.g., JlFO1d16b9)")
    parser.add_argument("message", help="Test message to send")
    parser.add_argument("--workspace-id", dest="workspace_id",
                        default=os.environ.get("DIAFLOW_WORKSPACE_ID"),
                        help="Workspace ID (or set DIAFLOW_WORKSPACE_ID)")
    parser.add_argument("--output", "-o", help="Output file path for debug report")
    parser.add_argument("--timeout", type=int, default=90,
                        help="Max seconds to wait for completion (default: 90)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print progress to stderr")
    args = parser.parse_args()

    token = os.environ.get("DIAFLOW_TOKEN")
    if not token:
        print("Error: DIAFLOW_TOKEN environment variable is not set", file=sys.stderr)
        sys.exit(1)

    def log(msg):
        if args.verbose:
            print(f"[debug] {msg}", file=sys.stderr)

    # Step 1: Fetch builder to get numeric ID
    log(f"Fetching builder {args.unique_id}...")
    status, builder = api_call("GET", f"/builders/{args.unique_id}", token)
    if not status or status >= 400:
        print(f"Error: Failed to fetch builder: {builder}", file=sys.stderr)
        sys.exit(1)

    numeric_id = builder.get("id")
    workspace_id = args.workspace_id or str(builder.get("workspaceId", ""))
    title = builder.get("title", "Unknown")
    log(f"Builder: {title} (id={numeric_id}, workspace={workspace_id})")

    if not workspace_id:
        print("Error: No workspace ID. Set DIAFLOW_WORKSPACE_ID or use --workspace-id", file=sys.stderr)
        sys.exit(1)

    # Step 2: Create conversation
    log("Creating test conversation...")
    conv_body = {
        "isTest": True,
        "defaultFirstMessage": [],
        "builderId": numeric_id,
        "type": "chat",
        "title": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    }
    status, conv = api_call("POST", "/conversations", token, workspace_id, conv_body)
    if not status or status >= 400:
        print(f"Error: Failed to create conversation: {conv}", file=sys.stderr)
        sys.exit(1)

    conv_id = conv.get("id")
    log(f"Conversation created: {conv_id}")

    # Step 3: Send message
    log(f"Sending message: {args.message[:50]}...")
    status, process = api_call(
        "POST", f"/conversations/{conv_id}/process",
        token, workspace_id, {"input": args.message}
    )
    if not status or status >= 400:
        print(f"Error: Failed to send message: {process}", file=sys.stderr)
        sys.exit(1)

    process_uuid = process.get("sessionId") or process.get("id")
    log(f"Processing started: {process_uuid}")

    # Step 4: Poll for completion
    start_time = time.time()
    poll_count = 0
    last_status = "Processing"
    completed_nodes = set()

    while time.time() - start_time < args.timeout:
        time.sleep(1)
        poll_count += 1

        status, check = api_call(
            "GET", f"/conversations/{conv_id}/process-checks/{process_uuid}",
            token, workspace_id
        )

        if not status or status >= 400:
            log(f"Poll error (attempt {poll_count}): {check}")
            continue

        last_status = check.get("status", "Unknown")

        # Track newly completed nodes (skip sticky notes — they always error)
        nodes = check.get("node", [])
        for node_entry in nodes:
            for node_id, node_data in node_entry.items():
                if node_id.startswith("stn-"):
                    continue
                if node_id not in completed_nodes and node_data.get("status") == "Done":
                    completed_nodes.add(node_id)
                    log(f"  Node completed: {node_id} ({node_data.get('time', '?')}s)")
                elif node_id not in completed_nodes and node_data.get("status") == "Error":
                    completed_nodes.add(node_id)
                    log(f"  Node FAILED: {node_id} — {node_data.get('message', 'unknown error')}")

        if last_status != "Processing":
            break

    elapsed = round(time.time() - start_time, 1)

    # Step 5: Build debug report
    report = {
        "builder": {
            "uniqueId": args.unique_id,
            "numericId": numeric_id,
            "title": title,
            "workspaceId": int(workspace_id)
        },
        "conversation": {
            "id": conv_id,
            "processUuid": process_uuid
        },
        "execution": {
            "status": last_status,
            "message": args.message,
            "elapsed_seconds": elapsed,
            "poll_count": poll_count,
            "timed_out": last_status == "Processing"
        },
        "nodes": [],
        "errors": [],
        "result_summary": {}
    }

    # Parse node results (skip sticky notes — they always error and are not functional)
    if "node" in check:
        for node_entry in check["node"]:
            for node_id, node_data in node_entry.items():
                if node_id.startswith("stn-"):
                    continue

                node_info = {
                    "id": node_id,
                    "status": node_data.get("status", "Unknown"),
                    "time": node_data.get("time"),
                    "metaContent": node_data.get("metaContent"),
                }
                # Include output summary (truncated for readability)
                output = node_data.get("output")
                if output is not None:
                    output_str = json.dumps(output) if not isinstance(output, str) else output
                    node_info["output_preview"] = output_str[:300]
                    if len(output_str) > 300:
                        node_info["output_truncated"] = True

                # Include error message
                msg = node_data.get("message")
                if msg:
                    node_info["error_message"] = msg

                report["nodes"].append(node_info)

                if node_data.get("status") == "Error":
                    report["errors"].append({
                        "node_id": node_id,
                        "message": msg or "Unknown error",
                        "metaContent": node_data.get("metaContent")
                    })

    # Summary
    total_nodes = len(report["nodes"])
    done_nodes = sum(1 for n in report["nodes"] if n["status"] == "Done")
    error_nodes = sum(1 for n in report["nodes"] if n["status"] == "Error")
    report["result_summary"] = {
        "total_nodes": total_nodes,
        "done": done_nodes,
        "errors": error_nodes,
        "processing": total_nodes - done_nodes - error_nodes,
        "total_step": check.get("total_step")
    }

    # Output
    report_json = json.dumps(report, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report_json)
        print(args.output)
    else:
        print(report_json)

    # Print summary to stderr
    status_emoji = "✓" if last_status == "Done" and error_nodes == 0 else "✗" if error_nodes > 0 else "?"
    print(f"\n{status_emoji} {last_status} in {elapsed}s — {done_nodes}/{total_nodes} nodes OK, {error_nodes} errors",
          file=sys.stderr)

    if report["errors"]:
        print("\nFailed nodes:", file=sys.stderr)
        for err in report["errors"]:
            print(f"  - {err['node_id']}: {err['message']}", file=sys.stderr)

    # Exit code
    if last_status == "Processing":
        sys.exit(2)  # Timeout
    elif error_nodes > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
