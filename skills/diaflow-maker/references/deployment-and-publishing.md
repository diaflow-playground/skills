# Deployment and Publishing Reference

## Publishing a Flow

To publish a flow, click the **Publish** button in the top-right corner of the Flow Builder. Ensure there are no errors in the flow before publishing.

After clicking Publish, three deployment options are available:

### 1. Internal Apps

- **Access**: Restricted to authenticated users within the workspace
- **Sharing**: Generates a shareable link for team members
- **Requirement**: Users must be logged into Diaflow to access the app
- **Use case**: Internal tools, team workflows, private dashboards

### 2. Public Apps

- **Access**: Unrestricted -- anyone with the link can use the app
- **Customizable appearance**:
  - Title
  - Subtitle
  - Logo
  - Cover image
  - Colors
  - Style
  - Input/output configuration
- **Security options**:
  - **Public** -- Open access via link, no authentication required
  - **Password-protected** -- Requires a password to access
- **Use case**: Customer-facing tools, public utilities, lead generation forms

### 3. Run via API

- **Access**: Execute the flow programmatically from external systems
- **Documentation**: Click the "API Docs" button to view endpoint details
- **Supported languages**: Python, JavaScript, cURL examples provided
- **Authentication**: Uses workspace API Keys
- **Use case**: Backend integrations, automated pipelines, third-party app connections

---

## Deployment (Chatbots Only)

Deployment options are available exclusively for AI Chatbot & Agent flows, enabling embedding into external websites.

### How to Deploy:

1. Open the flow in the Flow Editor
2. Click the **Deployment** icon
3. Choose from three embedding options:

### Embedding Options:

| Option | Description |
|--------|-------------|
| **Access link** | Direct URL to the chatbot interface |
| **Web gadget** | Floating chat widget that appears on your website |
| **iFrame code** | HTML iframe snippet for embedding the chatbot directly into any webpage |

### iFrame Embedding:
- Copy the provided iFrame code
- Paste it into your website's HTML where you want the chatbot to appear
- The chatbot renders within the iframe dimensions

---

## Unpublishing a Flow

Unpublishing is available only for **Apps** and **AI Agents/Chatbots** (not Automation flows).

Effects of unpublishing:
- The flow moves to **Draft** status
- All access is **deactivated and halted** immediately
- Internal app links stop working
- Public app links stop working
- API endpoints stop responding
- Deployed chatbot embeds stop functioning

To unpublish: Open the flow > access the publish/status menu > select **Unpublish**.

---

## Flow Management

### Filter Options

| Filter | Values |
|--------|--------|
| **Type** | Apps, Chats, Automation |
| **Status** | Published, Draft |

### Sort Options

- Last edit
- Latest date
- Earliest date
- Alphabet

### Actions by Flow Type and Status

| Status | Flow Type | Available Actions |
|--------|-----------|-------------------|
| **Draft** | All types | Edit, Rename, Duplicate, Delete |
| **Published** | Apps & Chats | Internal/Public app link, Edit, Duplicate, Unpublish, Configurations, Access Management, Delete |
| **Published** | Automation | Edit, Duplicate, Unpublish, Configurations, Delete |

### Deleting a Flow

- Available from: Dashboard Home Page, Flows Page, or Builder Flows Page
- Requires flow ID confirmation
- **Permanent action** -- once deleted, a flow cannot be restored
