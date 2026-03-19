#!/usr/bin/env python3
"""
Diaflow Workflow JSON Validator

Validates workflow JSON against Diaflow's expected format:
- Structural checks (required fields, types)
- Graph checks (connector integrity, reachability)
- Semantic checks (trigger/output existence, ID patterns)

Usage:
    python validate_workflow.py <file.json>
    cat workflow.json | python validate_workflow.py

Output: JSON with {valid, errors, warnings}
Exit code: 0 if valid, 1 if errors
"""

import json
import re
import sys
from collections import defaultdict


def validate(workflow):
    errors = []
    warnings = []

    # --- Structural Validation ---

    if not isinstance(workflow, dict):
        errors.append("Root must be a JSON object")
        return errors, warnings

    data = workflow.get("data")
    if data is None:
        # Accept both top-level {nodes, connectors} and nested {data: {nodes, connectors}}
        if "nodes" in workflow and "connectors" in workflow:
            data = workflow
        else:
            errors.append("Missing 'data' field (or top-level 'nodes'/'connectors')")
            return errors, warnings

    if not isinstance(data, dict):
        errors.append("'data' must be an object")
        return errors, warnings

    nodes = data.get("nodes")
    connectors = data.get("connectors")

    if nodes is None:
        errors.append("Missing 'data.nodes' array")
    elif not isinstance(nodes, list):
        errors.append("'data.nodes' must be an array")
        nodes = []

    if connectors is None:
        errors.append("Missing 'data.connectors' array")
    elif not isinstance(connectors, list):
        errors.append("'data.connectors' must be an array")
        connectors = []

    if errors:
        return errors, warnings

    if len(nodes) == 0:
        errors.append("Flow has no nodes")
        return errors, warnings

    # --- Node Validation ---

    node_ids = set()
    node_types = {}
    trigger_count = 0
    output_count = 0

    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"Node at index {i} is not an object")
            continue

        node_id = node.get("id")
        if not node_id:
            errors.append(f"Node at index {i} missing 'id' field")
            continue

        if node_id in node_ids:
            errors.append(f"Duplicate node ID: '{node_id}'")
        node_ids.add(node_id)

        node_type = node.get("type")
        if not node_type:
            errors.append(f"Node '{node_id}' missing 'type' field")
        else:
            node_types[node_id] = node_type

        # Position check
        position = node.get("position")
        if position is None:
            warnings.append(f"Node '{node_id}' missing 'position' field")
        elif isinstance(position, dict):
            if "x" not in position or "y" not in position:
                warnings.append(f"Node '{node_id}' position missing 'x' or 'y'")

        # Data field check
        node_data = node.get("data")
        if node_data is None:
            warnings.append(f"Node '{node_id}' missing 'data' field")
        elif isinstance(node_data, dict) and len(node_data) == 0:
            warnings.append(f"Node '{node_id}' has empty 'data' object")

        # Count trigger and output nodes
        if node_type == "trigger" or node_id == "trigger":
            trigger_count += 1
        if node_type == "output" or node_id == "output":
            output_count += 1

    # --- Connector Validation ---

    connector_ids = set()
    incoming = defaultdict(int)
    outgoing = defaultdict(int)

    for i, conn in enumerate(connectors):
        if not isinstance(conn, dict):
            errors.append(f"Connector at index {i} is not an object")
            continue

        conn_id = conn.get("id")
        if not conn_id:
            warnings.append(f"Connector at index {i} missing 'id' field")

        if conn_id and conn_id in connector_ids:
            warnings.append(f"Duplicate connector ID: '{conn_id}'")
        if conn_id:
            connector_ids.add(conn_id)

        source = conn.get("source")
        target = conn.get("target")

        if not source:
            errors.append(f"Connector '{conn_id or i}' missing 'source'")
            continue
        if not target:
            errors.append(f"Connector '{conn_id or i}' missing 'target'")
            continue

        if source not in node_ids:
            errors.append(f"Connector '{conn_id or i}' source '{source}' not found in nodes")
        if target not in node_ids:
            errors.append(f"Connector '{conn_id or i}' target '{target}' not found in nodes")

        if source == target:
            errors.append(f"Connector '{conn_id or i}' is a self-loop (source == target == '{source}')")

        conn_type = conn.get("type")
        if not conn_type:
            warnings.append(f"Connector '{conn_id or i}' missing 'type' field (expected 'smoothstep')")

        incoming[target] += 1
        outgoing[source] += 1

    # --- Semantic Validation ---

    # Trigger checks
    if trigger_count == 0:
        errors.append("No trigger node found (every flow needs exactly one trigger)")
    elif trigger_count > 1:
        errors.append(f"Found {trigger_count} trigger nodes (expected exactly 1)")

    # Trigger should have no incoming connectors
    if "trigger" in node_ids and incoming.get("trigger", 0) > 0:
        errors.append("Trigger node should not have incoming connectors")

    # Output check for non-automation flows
    if output_count == 0:
        warnings.append("No output node found (required for Apps and Chat flows, optional for Automation)")

    # Orphan node check (nodes with no connections except trigger)
    for node_id in node_ids:
        if node_id == "trigger":
            continue
        has_incoming = incoming.get(node_id, 0) > 0
        has_outgoing = outgoing.get(node_id, 0) > 0
        if not has_incoming and not has_outgoing:
            warnings.append(f"Node '{node_id}' is disconnected (no incoming or outgoing connectors)")
        elif not has_incoming:
            # Check if it's a path node (created by branch, connected via sourceHandle)
            node_type = node_types.get(node_id, "")
            if not node_id.startswith("path-") and node_type != "stn":
                warnings.append(f"Node '{node_id}' has no incoming connectors")

    # Node ID pattern check
    known_fixed_ids = {"trigger", "output"}
    id_pattern = re.compile(r"^[a-zA-Z_][\w-]*-\d+$")

    for node_id in node_ids:
        if node_id in known_fixed_ids:
            continue
        if node_id.startswith("path-"):
            continue  # Branch path nodes
        if not id_pattern.match(node_id):
            warnings.append(
                f"Node ID '{node_id}' doesn't follow expected pattern '{{type}}-{{index}}' "
                f"(e.g., 'openai-0', 'branch-0')"
            )

    # Branch-path consistency check
    branch_nodes = [nid for nid, ntype in node_types.items() if ntype == "branch"]
    path_nodes = [nid for nid in node_ids if nid.startswith("path-")]
    if branch_nodes and not path_nodes:
        warnings.append("Branch node(s) found but no path nodes (branch creates path-{n} nodes)")

    # Reachability check from trigger
    if "trigger" in node_ids and len(node_ids) > 1:
        # Build adjacency list
        adj = defaultdict(set)
        for conn in connectors:
            if isinstance(conn, dict) and conn.get("source") and conn.get("target"):
                adj[conn["source"]].add(conn["target"])

        # BFS from trigger
        visited = set()
        queue = ["trigger"]
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            for neighbor in adj.get(current, []):
                if neighbor not in visited:
                    queue.append(neighbor)

        unreachable = node_ids - visited
        if unreachable:
            # Filter out sticky notes and standalone nodes
            meaningful_unreachable = [
                nid for nid in unreachable
                if not node_types.get(nid, "").startswith("stn")
            ]
            if meaningful_unreachable:
                warnings.append(
                    f"Nodes unreachable from trigger: {', '.join(sorted(meaningful_unreachable))}"
                )

    return errors, warnings


def main():
    # Read input
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            with open(filepath, "r") as f:
                content = f.read()
        except FileNotFoundError:
            print(json.dumps({"valid": False, "errors": [f"File not found: {filepath}"], "warnings": []}))
            sys.exit(1)
        except IOError as e:
            print(json.dumps({"valid": False, "errors": [f"Cannot read file: {e}"], "warnings": []}))
            sys.exit(1)
    else:
        content = sys.stdin.read()

    # Parse JSON
    try:
        workflow = json.loads(content)
    except json.JSONDecodeError as e:
        print(json.dumps({"valid": False, "errors": [f"Invalid JSON: {e}"], "warnings": []}))
        sys.exit(1)

    # Validate
    errors, warnings = validate(workflow)

    result = {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }

    print(json.dumps(result, indent=2))
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
