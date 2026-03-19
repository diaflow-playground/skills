# Diaflow API Reference

Quick reference for all Diaflow API endpoints. For full schemas with all properties, read `diaflow-openapi.yaml`.

## Table of Contents
1. [Auth](#auth)
2. [Users](#users)
3. [Workspaces](#workspaces)
4. [Builders](#builders)
5. [Interfaces](#interfaces)
6. [Histories](#histories)
7. [Components & Node Configs](#components--node-configs)
8. [Templates & Community](#templates--community)
9. [Documents](#documents)
10. [Tables](#tables)
11. [Drive](#drive)
12. [Vectors](#vectors)
13. [Members](#members)
14. [API Keys](#api-keys)
15. [Integrations](#integrations)
16. [Products](#products)
17. [Conversations & Execution](#conversations--execution)
18. [Chat & Prompts](#chat--prompts)

---

## Auth

### POST /auth/login
No auth required. Body: `{ "email", "password" }`. Returns `{ "sessionToken", "user" }`.

> **Note:** The diaflow-maker skill uses the `$DIAFLOW_TOKEN` environment variable instead of calling this endpoint directly. Run `scripts/setup_token.sh` to set it up.

### POST /auth/logout
Invalidates session. No body needed.

### GET /auth/presign-token
Returns CloudFront signed cookie fields: `{ "Policy", "Signature", "Key-Pair-Id", "expires_at" }`.

---

## Users

### GET /users/me
Returns full user profile (~35 fields): id, username, email, fullName, avatar, role, accountType, credit, color, category, goalOptions, isActive, logo, phoneNumber, phoneCode, teamSize, companyName, companySize, location, onboardingData, defineYou, profileInfo, isPublicProfile, isProfileVerified, createdAt, updatedAt, etc.

### PATCH /users/me
Update profile fields. Body: `{ "fullName", "avatar", "username", ... }`.

---

## Workspaces

### GET /workspaces
Returns `{ total, results }` — list of workspaces with id, workspaceName, subdomain, role.

### GET /workspaces/{workspaceId}
Full workspace: resource counters (currentCredits, totalFlowsAmount, currentUsersAmount, totalStorageAmount, etc.), feature flags (featureRemoveLogo, featureCustomDomain), owner ref, appearance/meta config.

### GET /workspaces/{workspaceId}/me
Current user's membership: role, isOwner, lastLogin, builders count, user/owner refs.

### GET /workspaces/{workspaceId}/subscription
Subscription: plan, status, amount, cycle, validFrom, validTo, nextBilling, nested product object with all plan limits.

---

## Builders

### GET /workspaces/{workspaceId}/builders
Query: `page`, `pageSize`. Returns `{ total, results }`.
Each result: title, uniqueId, id, workspaceId, interfaceType, triggerType, version (draft/publish), isActive, enableAccess, enableApi, isSubflow, webhookEnable, runCount, createdAt, updatedAt, createdBy, interface, interfaceChat, data (with nodes/connectors).

### POST /builders
Create new builder. Body: `{ "title", "interfaceType", "workspaceId" }`.
interfaceType: `form` | `chat` | `automation` | `scheduled`.

### GET /builders/{uniqueId}
Full builder with data.nodes[], data.connectors[], and all metadata.

### PUT /builders/{numericId}
Update builder. **Must use numeric `id`, not `uniqueId`**. PATCH returns 405.
Body: any top-level fields to update (title, data, triggerType, etc.).

### DELETE /builders/{uniqueId}
Delete builder permanently.

### POST /builders/{uniqueId}/publish
Publish draft → live. Changes version from "draft" to "publish".

### POST /builders/{uniqueId}/execute
Execute a flow. Body: `{ "input": {}, "mode": "sync" }`.

---

## Interfaces

### GET /interfaces/{builderId}
Form/page interface config: components[], primaryColor, widgetTheme, banner, welcomeMessage, security, embedded builder object.

### GET /chat-interfaces/{builderId}
Chat interface config: title, tagline, logo, cover, widgetTheme, inputNode (object), openingQuestions, dataToCollect, embedded builder.

### GET /chat-interfaces/app/{appId}
Public chat interface by app ID. Only needs x-api-key (no Bearer token).

---

## Histories

### GET /workspaces/{workspaceId}/histories
Query: `page`, `pageSize`. Returns `{ total, results }`.
Each: id, builderId, sessionId, status, credit, latency, start, end, input, output, logType, models, via, builder ref, user ref, apiKey ref.

### GET /workspaces/{workspaceId}/histories/{historyId}
Same shape as list item. historyId is integer. Includes full action map with per-node data.

---

## Components & Node Configs

### GET /components
Returns `{ total, results }`. Each component: id (integer), title, description, nodeId, icon, isRoot, categories[], isPipedream, pipedream fields.

### GET /node-configs/model-configs
Returns object keyed by provider (openai, anthropic, mistral, vertex-ai, cohere, llama, byteplus, firecrawl, etc.). Each provider maps to array of model configs with name, model, max_token, model_type, is_active, params.

### GET /node-configs/component-prices
Returns `{ components: {} }` keyed by node_id. Each has prices map with input_cost, output_cost, unit, model, variant, priority.

---

## Templates & Community

### GET /template-categories
Returns `{ total, results }` with id, name, icon, description, background, isActive, priority.

### GET /templates/public
Query: `page`, `pageSize`. Returns `{ total, results }` with title, color, plan, data (flow graph), categories[], isDraft, used, icon, keyFeatures.

### GET /community/profile/me
Community profile: username, avatar, bio, templatesCount. Returns 404 if no profile.

### GET /badges/current
Returns a single announcement object (not array): title, category, content, redirectUrl, isActive.

---

## Documents

### GET /documents
Returns `{ total, results }`. Each: id, title, data (content), language, writingStyle, llmModel, llmProvider, uniqueId, isDraft, usage, creator/owner/lastEditor refs.

### POST /documents
Create page. Body: `{ "title", "data", "language", "writingStyle", "writingLength", "llmModel", "llmProvider" }`.

### GET /documents/config
Returns features list, llm_provider options, writing_style options, writing_length options.

---

## Tables

### GET /workspace-databases/{workspaceId}/tables
Returns flat array of `{ table_name, columns: [{ name, data_type }] }`. Lists all table schemas in the workspace.

### GET /workspace-db-tables/workspace/{workspaceId}
Query: `page`, `limit`, `filter`, `orderBy`. Returns `{ total, results }` with id, tableName, columnCount, rowCount, data, isActive, timestamps.

### POST /workspace-databases/{workspaceId}/ddl/tables
Create a new empty table. Body: `{}` (empty object). Returns the created table with auto-generated name (e.g., `table_35`). Rename afterward via `PUT /workspace-databases/{workspaceId}/sql` with `ALTER TABLE ... RENAME TO ...`.

### POST /workspace-databases/{workspaceId}/ddl/columns
Add a column to an existing table. Body:
```json
{
  "tableName": "table_35",
  "columnName": "created_date",
  "displayDataType": "date",
  "dataType": "timestamp with time zone",
  "isRequired": false,
  "defaultValue": "null"
}
```
Common `dataType` values: `character varying`, `text`, `real`, `integer`, `timestamp with time zone`, `boolean`.
Common `displayDataType` values: `single_line_text`, `long_text`, `number`, `date`, `checkbox`.

### PATCH /workspace-databases/{workspaceId}/ddl/columns/rename
Rename a column. Body: `{ "tableName", "oldColumnName", "newColumnName" }`.

### PATCH /workspace-databases/{workspaceId}/ddl/columns/config
Update column configuration. Body:
```json
{
  "tableName": "table_35",
  "columnName": "test",
  "newColumnName": "test",
  "displayDataType": "single_line_text",
  "dataType": "character varying",
  "isRequired": true,
  "defaultValue": "abc"
}
```

### POST /workspace-databases/{workspaceId}/tables/columns
Get column definitions for a table. Body: `{ "tableName": "table_35" }`.

### POST /workspace-databases/{workspaceId}/tables/items
Get rows from a table (paginated). Query: `page`, `limit`, `orderBy`, `filter`.
Body: `{ "tableName": "table_35" }`.
`orderBy` examples: `-diaflow_created_at` (descending), `name` (ascending).
`filter` is a URL-encoded JSON object (e.g., `{"status":"Pending"}`).

### POST /workspace-databases/{workspaceId}/dml/row
Insert a new row. Body:
```json
{
  "tableName": "table_35",
  "cellValuesByColumnName": {
    "name": "value1",
    "phone_number": "123",
    "created_date": null
  }
}
```

### PUT /workspace-databases/{workspaceId}/sql
Execute raw SQL (UPDATE, ALTER TABLE, etc.). Body: `{ "sql": "UPDATE \"table_35\" SET \"name\" = 'value' WHERE diaflow_id = 'uuid'" }`.
Also used for table rename: `{ "sql": "ALTER TABLE \"old_name\" RENAME TO \"new_name\";" }`.

### DELETE /workspace-databases/{workspaceId}/dml/row
Delete rows by ID. Body: `{ "tableName": "table_35", "rowIds": ["uuid1", "uuid2"] }`.

### PUT /workspace-databases/{workspaceId}/dml/row/clear
Clear (reset) row values. Body: `{ "tableName": "table_35", "rowIds": ["uuid1", "uuid2"] }`.

### POST /workspace-databases/{workspaceId}/csv-schema
Parse a CSV file schema before import. Body: `{ "file": "production/workspace_256/products.csv", "isTreatFirstRowAsHeader": true }`.
The file path references a file previously uploaded to Diaflow Drive.

### POST /workspace-databases/{workspaceId}/upsert-table
Import CSV data into a new or existing table. Body:
```json
{
  "tableName": "01_products",
  "isTreatFirstRowAsHeader": true,
  "isNewPrimaryKey": true,
  "usingPrimaryKey": "",
  "isNewTable": true,
  "file": "production/workspace_256/products.csv",
  "fields": [
    {"column": "id", "dataType": "real", "displayDataType": "number", "isNull": false, "isDisplayId": true, "isDisable": false},
    {"column": "name", "dataType": "text", "displayDataType": "long_text", "isNull": false, "isDisable": false},
    {"column": "price", "dataType": "real", "displayDataType": "number", "isNull": false, "isDisable": false}
  ]
}
```
**Note:** Table names starting with a letter may conflict with reserved names. Prefix with numbers (e.g., `01_products`) if needed.

### POST /workspace-databases/{workspaceId}/export
Export table data. Body: `{ "tableName": "table_35" }`. Returns CSV or downloadable content.

---

## Drive

### GET /drives/s3/directory
Returns `{ total, fileCount, folderCount, results }`. Each: id, fileName, fileExtension, fileSize, mimeType, parentFolder, isFolder, s3Key.

### POST /drives/s3/upload
Multipart form upload. Returns `{ key, url }`.

---

## Vectors

### GET /workspaces/{workspaceId}/vector-groups
Returns `{ total, results }` with title, workspaceId, numVector, used.

### GET /workspaces/{workspaceId}/vectors
Returns `{ total, results }`. Each vector: type (Document/Article/Website), name, url, file, status, groups[], log, config, size.

### POST /vector-groups
Create knowledge base. Body: `{ "name", "description", "workspaceId" }`.

### GET /vector-groups/{groupId}
Vector group detail with description, vectorCount, timestamps.

### GET /vector-groups/{groupId}/vector-ids
List vector IDs and metadata within a group.

### POST /vectors/stream/{workspaceId}
Similarity search. Body: `{ "query", "groupId", "topK": 5 }`. Returns `{ results: [{ id, content, score, metadata }] }`.

---

## Members

### GET /workspaces/{workspaceId}/members
Returns `{ total, results }`. Each: id, email, role (owner/admin/member/viewer), status, isActive, lastLogin, builders, user ref.

### POST /workspaces/{workspaceId}/members/invite
Body: `{ "email", "role" }`. Returns `{ inviteId, email, status: "pending" }`.

---

## API Keys

### GET /workspaces/{workspaceId}/api-keys
Returns `{ total, results }`. Each: id (integer), name, key (full value), numUsed, lastUsed, userId, workspaceId.

### POST /workspaces/{workspaceId}/api-keys
Body: `{ "name" }`. Returns created key with full key value.

### DELETE /workspaces/{workspaceId}/api-keys/{keyId}
keyId is integer. Returns 204.

---

## Integrations

### GET /workspaces/{workspaceId}/integrations
List third-party integrations. May return 404 if not available for workspace.

### POST /workspaces/{workspaceId}/integrations
Body: `{ "type", "name", "config": {} }`.

---

## Products

### GET /products/{productId}
Product/plan details: name, internalId, billingTag, productType, fixedCredit, monthlyRenewed, creditsGranted, priority, label, resource limits (totalFlowsAmount, totalUsersAmount, etc.), feature flags, pricing.

---

## Conversations & Execution

### POST /conversations
Create a new conversation session for a chat flow preview/execution.
Body: `{ "builderId": "uniqueId", "input": {} }`.
Returns conversation object with `id` (integer, e.g., `180111`).

### POST /conversations/{conversationId}/process
Send a message or trigger flow execution within a conversation.
Body: `{ "message": "user input text" }`.
Returns a process UUID for polling (e.g., `814d88d9-f831-4afe-9423-1fa8d6ed4e87`).

### GET /conversations/{conversationId}/process-checks/{processUuid}
Poll for execution completion. Called repeatedly (~1s interval) until the flow finishes.
Returns execution status with per-node results:
- `status`: "running" | "completed" | "failed"
- Node-by-node output data, status, and errors
- On completion: final bot response message

**Execution flow pattern:**
1. `POST /conversations` → get conversationId
2. `POST /conversations/{id}/process` → get processUuid
3. `GET /conversations/{id}/process-checks/{uuid}` → poll until done (repeat every ~1s)

> **Note:** Preview mode uses HTTP polling, not WebSockets. Complex flows with multiple AI nodes can take 30-40+ seconds. Individual nodes (especially OpenAI) may timeout.

---

## Chat & Prompts

### GET /chat-preset-styles
Returns `{ total, results }` with id, name, prompt, isDefault, isAdminPreset.

### GET /agent-chat-windows
Returns `{ total, results }` with builderId, config.

### GET /sample-prompt-categories
Returns `{ total, results }` with id, name, type (shortcut/tools), nodeId, status, priority.

### GET /prompt-samples/llm
Returns `{ total, results }` with id, title, llmNode, promptType, nameValues[], promptValues[], descriptionValues[].
