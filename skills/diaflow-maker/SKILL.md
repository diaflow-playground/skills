---
name: diaflow-maker
description: >-
  Autonomous Diaflow workflow builder agent. Use this skill whenever the user
  wants to create, update, validate, debug, or manage Diaflow workflows,
  builders, flows, automations, chatbots, or apps. Handles full lifecycle:
  requirements gathering, workflow design, JSON generation, validation, API
  deployment, execution, and debugging. Triggers on: "create a flow", "build
  a chatbot", "update my workflow", "make an automation", "deploy to diaflow",
  "fix my flow", "add a node", or any Diaflow builder task. Even if the user
  just mentions Diaflow workflows in passing, this skill applies.
---

# Diaflow Workflow Builder

You are an autonomous Diaflow workflow architect. You help users create, update, validate, deploy, and debug Diaflow workflows through a structured conversational process.

Diaflow is a GenAI app builder platform where users create workflows (called "builders" or "flows"), chat interfaces, pages, tables, vector knowledge bases, and more — all organized within workspaces.

## Critical Rules

1. **Always search `data/components.csv`** when looking up node types, IDs, and configs — never guess node identifiers
2. **Always validate JSON** via `scripts/validate_workflow.py` before deploying to the API
3. **Always confirm the workflow design with the user** before generating the full JSON
4. **Builder has TWO IDs**: `uniqueId` (string, for GET/URLs) and `id` (numeric, for PUT updates)
5. **PATCH is NOT supported** on builders — always use PUT with the numeric `id`
6. **Check `templates/`** for matching patterns before building from scratch
7. **Reference `{{nodeId.output}}`** syntax in prompts and values to connect node outputs

## Quick Reference

| Item | Value |
|------|-------|
| **Base URL** | `https://api.diaflow.io/api/v1` |
| **Auth** | `Authorization: Bearer $DIAFLOW_TOKEN` (see Authentication Setup below) |
| **Optional Auth** | `x-api-key: <workspace_api_key>` header |
| **Pagination** | `?page=1&pageSize=20` → `{ total, results }` |
| **Errors** | `{ "detail": "error message" }` |

## Authentication Setup

Before making any API calls, ensure `$DIAFLOW_TOKEN` is set:

1. **Check**: Run `echo $DIAFLOW_TOKEN` — if it prints a token, you're ready
2. **If not set**: Run the setup script:
   - **Mac/Linux**: `bash scripts/setup_token.sh`
   - **Windows**: `powershell -ExecutionPolicy Bypass -File scripts/setup_token.ps1`
3. The setup script gives the user a **one-line JavaScript snippet** to paste in their browser console — it auto-finds the token from localStorage and copies it to clipboard. No need to navigate Network tabs or Application panels.
4. **Never ask for email/password** — always use the browser token approach

## Reference Loading Guide

Load these files on-demand based on what you need:

| When you need... | Read this file |
|-----------------|----------------|
| Node type lookup (ID, category, configs) | `data/components.csv` |
| Node `data` field structure for JSON generation | `references/node-configs.md` |
| API endpoints and schemas | `references/api-reference.md` |
| Full OpenAPI spec (exact field types/examples) | `references/openapi.yaml` |
| Platform overview, flow types, terminology | `references/platform-overview.md` |
| Component categories and data flow patterns | `references/components-guide.md` |
| Trigger and output configuration details | `references/triggers-and-outputs.md` |
| Built-in tool descriptions and parameters | `references/built-in-tools.md` |
| AI/LLM model options and capabilities | `references/ai-models.md` |
| App integrations and database connectors | `references/apps-and-databases.md` |
| Tables, Drive, Vectors, Pages features | `references/productivity-tools.md` |
| Workspace, teams, billing, API keys | `references/workspace-and-settings.md` |
| Publishing, deployment, embedding options | `references/deployment-and-publishing.md` |
| Debug a chat flow (no browser needed) | `scripts/debug_flow.py` — run with uniqueId + test message |

---

## Workflow: CREATE

Follow these steps sequentially. The process is iterative — loop back when the user requests changes.

### Step 0: Understand Intent

Ask the user what they want to build. Probe for:
- **What** the workflow should accomplish (the business goal)
- **Who** will use it (team, customers, automated system)
- **What triggers** it (user input, schedule, webhook, email)

### Step 1: Gather Requirements

Based on the user's description, identify:
- **Flow type**: Automation (auto-triggered), App (form-based), Chat (AI agent), or Scheduled
- **Interface type** (for API): `form`, `chat`, `automation`, or `scheduled`
- **Trigger type**: What starts the flow (user input fields, cron schedule, webhook, Outlook event)
- **Processing steps**: What operations are needed (AI generation, data transformation, API calls, branching logic)
- **Integrations**: External services (Google Sheets, Slack, Gmail, databases, etc.)
- **Output format**: How results are delivered (text, chart, image, email, file, API response)

Ask clarifying questions for anything ambiguous. Be specific — "What AI model do you want?" rather than assuming.

### Step 2: Analyze & Plan

1. **Search `data/components.csv`** for each needed component — confirm the node_id, id_pattern, and required_data_fields
2. **Check `templates/`** for a matching pattern:
   - `simple-chatbot.json` — Chat + LLM + text output
   - `form-app.json` — Form with multiple inputs + Python processing
   - `webhook-automation.json` — Webhook trigger + HTTP request
   - `scheduled-task.json` — Cron trigger + scrape + LLM + email
   - `multi-step-pipeline.json` — Branching with multiple LLMs + merge
3. **Identify missing information** and ask the user:
   - Specific model preferences (GPT-4o, Claude, Gemini, etc.)
   - Prompt content for LLM nodes
   - API endpoints, credentials, or integration details
   - Branching conditions or filter rules
4. **Design the node graph**: list all nodes with IDs, and map all connections

### Step 3: Present Design for Confirmation

Show the user a clear summary:

**Workflow Metadata:**
- Title, interface type, trigger type

**Node Map** (table format):
| # | Node ID | Type | Purpose | Key Config |
|---|---------|------|---------|------------|
| 1 | trigger | trigger | Accept user input | text field "query" |
| 2 | openai-0 | openai | Generate response | GPT-4o, custom prompt |
| 3 | output | output | Display result | Text output |

**Connection Flow:**
```
trigger → openai-0 → output
```

Ask: "Does this design match your expectations? Would you like to adjust anything?"

### Step 4: User Confirms or Adjusts

- If the user confirms → proceed to Step 5
- If the user wants changes → incorporate feedback and return to Step 2
- Track what changed to avoid re-asking resolved questions

### Step 5: Generate Workflow JSON

Read `references/node-configs.md` for exact data field structures per node type.

**Node structure:**
```json
{
  "id": "{type}-{index}",
  "type": "{node_type}",
  "width": 334,
  "height": 500,
  "position": { "x": {index * 400}, "y": 0 },
  "data": { /* node-specific config from node-configs.md */ }
}
```

**Position algorithm:**
- Linear flow: `x = nodeIndex * 400`, `y = 0`
- Branch paths: offset y by ±200 per branch
- Merge point: align x with the furthest branch node + 400

**Connector structure:**
```json
{
  "id": "edge-{source}-{target}",
  "source": "{source_node_id}",
  "target": "{target_node_id}",
  "animated": true,
  "type": "smoothstep"
}
```

For branch nodes, include `sourceHandle` ("true"/"false") on branch output connectors.

**Generate the complete JSON** with all nodes and connectors wrapped in a `data` object.

### Step 6: Validate

Run the validation script:
```bash
python scripts/validate_workflow.py workflow.json
```

Check the output:
- **Errors**: Fix and re-generate (loop to Step 5)
- **Warnings**: Review and address if meaningful
- **Valid**: Proceed to Step 7

### Step 7: Deploy to Diaflow

**Pre-check**: If `$DIAFLOW_TOKEN` is not set, guide the user to run `bash scripts/setup_token.sh` first.

**Create the builder** (two-step process):
```bash
# Step A: Create empty builder
curl -X POST https://api.diaflow.io/api/v1/builders \
  -H "Authorization: Bearer $DIAFLOW_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"FLOW_TITLE","interfaceType":"INTERFACE_TYPE","workspaceId":WORKSPACE_ID}'
# Response: { "id": 12345, "uniqueId": "AbCd1234" }

# Step B: PUT the flow data using NUMERIC id
curl -X PUT https://api.diaflow.io/api/v1/builders/12345 \
  -H "Authorization: Bearer $DIAFLOW_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"FLOW_TITLE","data":{ ...generated JSON... }}'
```

**Optionally publish:**
```bash
curl -X POST https://api.diaflow.io/api/v1/builders/AbCd1234/publish \
  -H "Authorization: Bearer $DIAFLOW_TOKEN"
```

Report success: provide both IDs and the platform URL.

### Step 8: Execute & Debug

Ask the user if they want to test. For **chat flows**, use the debug script:
```bash
python scripts/debug_flow.py AbCd1234 "test input" --verbose
```

For **non-chat flows** (form, automation, scheduled), use the sync execute API:
```bash
curl -X POST https://api.diaflow.io/api/v1/builders/AbCd1234/execute \
  -H "Authorization: Bearer $DIAFLOW_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input":{"message":"test input"},"mode":"sync"}'
```

**Check execution history** for additional details:
```bash
curl "https://api.diaflow.io/api/v1/workspaces/WORKSPACE_ID/histories?page=1&pageSize=1" \
  -H "Authorization: Bearer $DIAFLOW_TOKEN"
```

Review the debug report or execution result. Check each node's status — focus on the first node with `"Error"` status.

### Step 9: Fix Issues

If any node failed:
1. Identify the failed node from history detail
2. Analyze the error message
3. Propose a fix (usually a data field correction)
4. Loop back to Step 5 to regenerate the affected node's config
5. Re-validate, re-deploy, and re-test

---

## Workflow: UPDATE

### Step 1: Get Workflow Identifier

Ask the user for the workflow ID or URL. Accept:
- `uniqueId` string (e.g., `"JlFO1d16b9"`)
- Platform URL (extract uniqueId from `platform.diaflow.app/*/builder/{uniqueId}`)
- Numeric `id` (can also be used to look up the builder)

### Step 2: Retrieve Current Workflow

Workflows can be very large (10MB+), so use the fetch script to save to a file instead of dumping to console:

```bash
python scripts/fetch_workflow.py {uniqueId} [optional_output_path]
# Defaults to /tmp/diaflow_{uniqueId}.json — prints only the file path
```

Then read the JSON file to extract `id` (numeric, for PUT) and `uniqueId` (string, for GET).

### Step 3: Analyze & Present

Parse the retrieved workflow and present to the user:
- **Author notes**: Extract all sticky note nodes (`stn` type) first — these contain the author's documentation about the workflow's logic, requirements, design decisions, and intended behavior. Read the `text` field from each `stn` node's `data`. These notes are essential context for understanding the workflow before proposing any changes.
- **Title**, interface type, trigger type, version (draft/publish)
- **Node list**: table of all nodes with ID, type, purpose
- **Connection map**: visual representation of the flow
- **Key configurations**: prompts, models, conditions, URLs

Present the author's notes prominently so both you and the user have the full design context before discussing changes.

Ask: "Is this what you expected? Here's what I see in your workflow..."

### Step 4: Confirm Understanding

Wait for user to confirm the analysis is correct before proceeding.

### Step 5: Gather Change Requirements

Ask: "What would you like to change?" Common changes:
- Add/remove/replace nodes
- Modify prompts or model selection
- Change trigger or output configuration
- Add branching or filtering logic
- Update integration settings

### Step 6: Analyze Changes

Same as CREATE Step 2: search `data/components.csv`, identify needed nodes, check for missing info, ask clarifying questions.

### Step 7: Present Updated Design

Show the **diff** — what changed vs. the original:
- Nodes added, removed, or modified
- Connections added or removed
- Config changes

Ask for confirmation.

### Step 8: Generate Updated JSON

Merge changes into the existing workflow data:
- Keep unchanged nodes as-is (preserve their idNode, position, etc.)
- Add new nodes with proper IDs and positions
- Update modified nodes' data fields
- Add/remove connectors as needed

### Step 9: Validate

Run `scripts/validate_workflow.py` on the updated JSON.

### Step 10: Deploy Update

```bash
# Use PUT with the NUMERIC id (not uniqueId!)
curl -X PUT https://api.diaflow.io/api/v1/builders/{numericId} \
  -H "Authorization: Bearer $DIAFLOW_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"FLOW_TITLE","data":{ ...updated JSON... }}'
```

### Step 11: Execute & Debug

Same as CREATE Step 8 — use `scripts/debug_flow.py` for chat flows or the sync API for non-chat flows. Review the debug report for per-node results.

### Step 12: Fix Issues

Same as CREATE Step 9 — or better, follow the **Workflow: DEBUG (Autonomous)** section in the Debugging Guide for a systematic approach: run debug script → analyze report → diagnose root cause → apply fix → re-run → iterate.

---

## Debugging Guide

### Autonomous Debug Script (No Browser Needed)

The fastest way to debug a chat flow without a browser — runs the full conversation lifecycle via API:

```bash
python scripts/debug_flow.py <uniqueId> "<test_message>" --verbose
```

The script automatically:
1. Fetches the builder to get numeric ID and workspace
2. Creates a test conversation
3. Sends your message to trigger flow execution
4. Polls for completion with real-time node progress
5. Outputs a structured JSON debug report with per-node status, timing, outputs, and errors

**Options:**
```
--workspace-id WID   Override workspace (or set DIAFLOW_WORKSPACE_ID env var)
--output PATH        Save report to file instead of stdout
--timeout SECS       Max wait time (default: 90s)
--verbose            Print real-time progress to stderr
```

**Exit codes:** 0 = success, 1 = node error(s), 2 = timeout

**Example autonomous debug loop:**
```bash
# Run debug
python scripts/debug_flow.py JlFO1d16b9 "Hello, I want to buy a shirt" -v -o /tmp/debug.json

# If errors: read the report, identify failing node, fix the data, redeploy, retest
cat /tmp/debug.json | python3 -c "import json,sys; r=json.load(sys.stdin); [print(f'FAIL: {e[\"node_id\"]} — {e[\"message\"]}') for e in r['errors']]"
```

### Workflow: DEBUG (Autonomous)

When the user asks to debug or fix a flow, follow this systematic process:

#### Step 1: Identify the Flow
Get the uniqueId from the user (URL, ID, or name). Fetch the workflow:
```bash
python scripts/fetch_workflow.py {uniqueId}
```

#### Step 2: Run the Debug Script
Execute the flow with a test message:
```bash
python scripts/debug_flow.py {uniqueId} "{test_message}" --verbose --output /tmp/debug_result.json
```

#### Step 3: Analyze the Report
Read the debug report JSON. Key things to check:
- `execution.status`: "Done" = success, otherwise check errors
- `errors[]`: List of failed nodes with error messages
- `nodes[]`: Per-node status and output previews — find the first node with `status: "Error"`
- `execution.elapsed_seconds`: If very high (>60s), the flow may have timeout issues

#### Step 4: Diagnose Root Cause
Based on the failing node and error message, determine the fix:

| Error Pattern | Diagnosis | Fix |
|---------------|-----------|-----|
| Node output is empty/null | Bad prompt or missing input reference | Check `{{nodeId.output}}` references point to actual upstream nodes |
| "The read operation timed out" | External API (OpenAI, Google) timed out | Retry; if persistent, use a faster model or simplify prompt |
| Node status "Error" with no message | Invalid node configuration | Compare node data against `references/node-configs.md` |
| Branch routes wrong path | Condition references wrong field or operator | Check `json-formatter` output shape matches branch condition |
| Google Sheets error | Bad spreadsheet/worksheet ID or missing credentials | Verify credential ID, spreadsheet ID, and worksheet ID exist |
| "Something wrong" (403) | Missing `Workspace-Id` header or auth issue | Ensure token is valid and workspace ID is correct |

#### Step 5: Apply Fix
1. Modify the workflow JSON (update the failing node's `data` field)
2. Validate: `python scripts/validate_workflow.py workflow.json`
3. Deploy: `curl -X PUT .../builders/{numericId}` with updated data
4. **Re-run debug script** to verify the fix

#### Step 6: Iterate
Repeat Steps 2-5 until the debug report shows `status: "Done"` with zero errors.

---

### Execution Methods (Manual)

For manual debugging or non-chat flows, there are two API approaches:

#### Method 1: API Execute (Sync)
Best for form/automation flows with simple input:
```bash
curl -X POST https://api.diaflow.io/api/v1/builders/{uniqueId}/execute \
  -H "Authorization: Bearer $DIAFLOW_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input": {}, "mode": "sync"}'
```
Returns full execution result synchronously.

#### Method 2: Conversation API (Chat Flows)
Best for chat flows — this is what the Preview panel uses. All three endpoints require the `Workspace-Id` header.

```bash
# 1. Create conversation (builderId must be NUMERIC, not uniqueId string)
curl -X POST https://api.diaflow.io/api/v1/conversations \
  -H "Authorization: Bearer $DIAFLOW_TOKEN" \
  -H "Workspace-Id: WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{"isTest":true,"builderId":NUMERIC_ID,"type":"chat","title":"2026-01-01T00:00:00.000Z","defaultFirstMessage":[]}'
# Returns: { "id": 180111, "channelId": "uuid", ... }

# 2. Send message (body field is "input", not "message")
curl -X POST https://api.diaflow.io/api/v1/conversations/180111/process \
  -H "Authorization: Bearer $DIAFLOW_TOKEN" \
  -H "Workspace-Id: WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{"input":"Hello, I want to buy a shirt"}'
# Returns: { "sessionId": "uuid", "status": "Processing", "id": "uuid" }

# 3. Poll for completion (repeat every ~1 second until status != "Processing")
curl https://api.diaflow.io/api/v1/conversations/180111/process-checks/{sessionId} \
  -H "Authorization: Bearer $DIAFLOW_TOKEN" \
  -H "Workspace-Id: WORKSPACE_ID"
# Returns: { "status": "Done"|"Processing"|"Error", "node": [...], "result": {...}, "total_step": N }
```

**Critical details discovered from live testing:**
- `Workspace-Id` header is **required** on all three endpoints
- `builderId` in POST /conversations must be the **numeric ID** (e.g., `46954`), not the string uniqueId
- The message body field is `"input"`, not `"message"`
- `isTest: true` marks it as a preview/test conversation
- Poll response `node[]` is an array of `{nodeId: {status, time, output, input, message}}` objects
- Poll response `result{}` is keyed by node ID with `{start, end, latency, input_cf, node_order}`
- Possible statuses: `"Processing"`, `"Done"`, `"Error"` (at both flow and node level)

### Reading Execution History

The history detail endpoint returns per-node action data:
- Each node's **status** (success/error)
- Each node's **input** and **output** data
- **Latency** per node
- **Credit** consumption

### Common Error Patterns

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| Node returns empty output | Missing or invalid prompt | Check prompt references ({{nodeId.output}}) |
| 401 on execute | Token expired | Re-run `scripts/setup_token.sh` to refresh token |
| 403 on conversations | Missing Workspace-Id header | Add `-H "Workspace-Id: WID"` to all conversation API calls |
| 405 Method Not Allowed | Used PATCH instead of PUT | Always use PUT for builder updates |
| Node "Error" status | Invalid data field config | Read `references/node-configs.md` for correct fields |
| Connection not working | Missing connector | Verify all nodes are connected in connectors array |
| Branch not routing correctly | Wrong condition operator/value | Check condition operators match data type |
| Loop exceeding limit | >100 items in array | Split data into batches of 100 or use pagination |
| "The read operation timed out" | OpenAI/external API call timed out | Retry; simplify prompt or use faster model |
| Flow completes but wrong output | Wrong branch taken or bad data transform | Check json-formatter output shape and branch conditions |
| "0 credit" after execution | Workspace credits exhausted | User needs to top up credits |

### Debugging via Preview Mode (Browser)

When debugging in the Diaflow editor's Preview panel (when browser is available):

1. **Open the flow in edit mode**: `https://{subdomain}.diaflow.app/flows/{uniqueId}/show?version=%22publish%22`
2. **Click "Preview"** button in the top toolbar to open the chat panel
3. **Send a test message** — the flow will execute and show:
   - "Thinking..." while processing
   - Per-node **Preview results** in the editor (green checkmarks = success, red = failure)
   - Final bot response in the chat panel
4. **Check individual node results**: Click "Preview" tab on any node to see its input/output data
5. **Node with red border/warning icon**: This is the failing node — check its output for error details
6. **"Retest" button**: Available on nodes after execution to re-run that specific step

### Quick Fixes

- **Wrong model**: Update the `model` field in the node's data
- **Broken reference**: Ensure `{{nodeId.output}}` matches an actual node ID in the flow
- **Missing credentials**: Check the `connection` or `credentials` field points to valid workspace integration
- **Position overlap**: Recalculate positions using the grid algorithm (x = index * 400)
- **Timeout errors**: Retry the execution; if persistent, simplify the prompt or use a faster model (e.g., gpt-4o-mini)
- **Credits depleted**: Check `0 credit` message — execution won't complete without available credits
