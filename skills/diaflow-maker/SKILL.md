---
name: diaflow
description: >-
  How to interact with the Diaflow API to manage workspaces, builders (flows),
  interfaces, documents, tables, vectors, and more. Use this skill whenever the
  user mentions Diaflow, asks about creating/cloning/updating flows or builders,
  managing workspaces, or interacting with api.diaflow.io. Also use when the
  user wants to automate Diaflow operations, query execution histories, manage
  team members, or work with Diaflow's vector knowledge bases, pages, or tables.
  Even if the user just says "create a chatbot" or "clone that flow" in a
  Diaflow project context, this skill applies.
---

# Diaflow API Skill

Diaflow is a GenAI app builder platform where users create workflows (called "builders" or "flows"), chat interfaces, pages, tables, vector knowledge bases, and more — all organized within workspaces.

## Quick Reference

- **Base URL**: `https://api.diaflow.io/api/v1`
- **Auth**: `Authorization: Bearer <JWT>` header (from `/auth/login`)
- **Optional**: `x-api-key: <workspace_api_key>` header
- **Full OpenAPI spec**: `references/openapi.yaml` — read this when you need exact request/response schemas, property types, required fields, or example values for any endpoint

## Authentication

```bash
# Login to get a JWT
curl -X POST https://api.diaflow.io/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret"}'
# Response: { "sessionToken": "eyJ...", "user": { "id": 123, ... } }
```

All subsequent requests need `Authorization: Bearer <sessionToken>`.

## Critical API Quirks

These behaviors differ from what you might expect and were discovered through real API testing:

### Builder IDs: Two Different IDs

Every builder has two identifiers:
- **`id`** (integer, e.g. `46904`) — used for **PUT updates**
- **`uniqueId`** (string, e.g. `"JlFO1d16b9"`) — used for **GET by ID** and in URLs

```
GET    /builders/{uniqueId}     ← string uniqueId
PUT    /builders/{numericId}    ← integer id
POST   /builders                ← creates new, returns both IDs
PATCH  /builders/{id}           ← returns 405 Method Not Allowed!
```

PATCH is **not supported** on builders. Always use PUT with the numeric `id`.

### Pagination Format

All paginated endpoints return `{ total, results }` — not `{ items }`:

```json
{
  "total": 154,
  "results": [{ ... }, { ... }]
}
```

Query params: `?page=1&pageSize=20`

### Error Response Shape

All errors return: `{ "detail": "error message" }`

Common errors:
- 401: `{"detail": "Not authenticated"}`
- 403: `{"detail": "You do not have permission to access this workspace."}`
- 404: `{"detail": "Not found"}`

## Common Workflows

### Clone / Duplicate a Builder

This is a two-step process because you can't create a builder with flow data in one call:

```bash
# Step 1: Create empty builder
curl -X POST https://api.diaflow.io/api/v1/builders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Cloned Flow",
    "interfaceType": "chat",
    "workspaceId": 256
  }'
# Response includes both id (integer) and uniqueId (string)

# Step 2: GET the source builder's full data
curl https://api.diaflow.io/api/v1/builders/{sourceUniqueId} \
  -H "Authorization: Bearer $TOKEN" > source.json

# Step 3: PUT the flow data onto the new builder using its NUMERIC id
curl -X PUT https://api.diaflow.io/api/v1/builders/{newNumericId} \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Cloned Flow","data":{ ...from source... }}'
```

The `data` field contains the entire flow graph:
- `data.nodes[]` — flow nodes (trigger, openai, branch, output, etc.)
- `data.connectors[]` — edges connecting nodes

### Create a New Builder

```bash
curl -X POST https://api.diaflow.io/api/v1/builders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My New Flow",
    "interfaceType": "chat",
    "workspaceId": 256
  }'
```

`interfaceType` values: `"form"`, `"chat"`, `"automation"`, `"scheduled"`

### List Builders in a Workspace

```bash
curl "https://api.diaflow.io/api/v1/workspaces/256/builders?page=1&pageSize=20" \
  -H "Authorization: Bearer $TOKEN"
```

### Publish a Builder

```bash
curl -X POST https://api.diaflow.io/api/v1/builders/{uniqueId}/publish \
  -H "Authorization: Bearer $TOKEN"
```

Changes `version` from `"draft"` to `"publish"`.

### Execute a Builder

```bash
curl -X POST https://api.diaflow.io/api/v1/builders/{uniqueId}/execute \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input": {"message": "Hello"}, "mode": "sync"}'
```

## Builder Data Structure

A builder's `data` field contains the flow graph:

```json
{
  "data": {
    "nodes": [
      {
        "id": "trigger",
        "type": "trigger",
        "width": 334,
        "height": 457,
        "position": { "x": 0, "y": 0 },
        "data": { /* node-specific config */ }
      },
      {
        "id": "openai-0",
        "type": "openai",
        "data": { "model": "gpt-4", "prompt": "..." }
      }
    ],
    "connectors": [
      {
        "id": "edge-trigger-openai-0",
        "source": "trigger",
        "target": "openai-0",
        "animated": true,
        "type": "smoothstep"
      }
    ]
  }
}
```

Common node types: `trigger`, `openai`, `anthropic`, `branch`, `path-*`, `output`, `py-*`, `json-formatter-*`, `google_sheets_p-*`, `stn-*`

## Key Endpoints by Category

For endpoint summaries, read `references/api-reference.md`. For exact request/response schemas, property types, and example values, read `references/openapi.yaml`.

| Category | Key Endpoints |
|----------|---------------|
| **Auth** | `POST /auth/login`, `POST /auth/logout`, `GET /auth/presign-token` |
| **Users** | `GET /users/me`, `PATCH /users/me` |
| **Workspaces** | `GET /workspaces`, `GET /workspaces/{id}`, `GET /workspaces/{id}/me`, `GET /workspaces/{id}/subscription` |
| **Builders** | `GET/POST /builders`, `GET/PUT/DELETE /builders/{id}`, `POST /builders/{id}/publish`, `POST /builders/{id}/execute` |
| **Interfaces** | `GET /interfaces/{builderId}`, `GET /chat-interfaces/{builderId}`, `GET /chat-interfaces/app/{appId}` |
| **Histories** | `GET /workspaces/{id}/histories`, `GET /workspaces/{id}/histories/{historyId}` |
| **Components** | `GET /components`, `GET /node-configs/model-configs`, `GET /node-configs/component-prices` |
| **Documents** | `GET/POST /documents`, `GET /documents/config` |
| **Tables** | `GET /workspace-databases/{id}/tables`, `GET /workspace-db-tables/workspace/{id}` |
| **Vectors** | `GET /workspaces/{id}/vector-groups`, `GET /workspaces/{id}/vectors`, `POST /vector-groups`, `POST /vectors/stream/{id}` |
| **Members** | `GET /workspaces/{id}/members`, `POST /workspaces/{id}/members/invite` |
| **API Keys** | `GET/POST /workspaces/{id}/api-keys`, `DELETE /workspaces/{id}/api-keys/{keyId}` |
| **Templates** | `GET /template-categories`, `GET /templates/public` |

## Tips

- When you need exact request/response schemas, property types, required fields, or example values, read `references/openapi.yaml`. It has 54 schemas with real examples for all 53 API operations.
- When cloning builders, the `data` field can be very large (1MB+). This is normal — it contains the full flow graph with all node configurations.
- Builder `version` values: `"draft"` (editable) or `"publish"` (live).
- The `createdBy` field on builders is a nested user object, not just an ID.
- Workspace resource counters (`currentCredits`, `totalFlowsAmount`, etc.) reflect real-time usage.
- Vector groups are Diaflow's knowledge bases. Vectors within groups can be of type `"Document"`, `"Article"`, or `"Website"`.
