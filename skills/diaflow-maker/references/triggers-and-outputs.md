# Triggers and Outputs Reference

## Triggers Overview

Triggers are the entry points that initiate a flow. The trigger type depends on the flow type:
- **Apps & Tools** -- Apps trigger (form-based input fields)
- **Automation** -- Scheduled time, Webhook, or Microsoft Outlook
- **AI Agent/Chatbots** -- AI Chat & Agent trigger

---

## Apps Trigger (When Inputs Are Submitted)

The Apps trigger supports **8 input field types**, each with configurable parameters:

### 1. Short Text
- **Parameters**: Input Label, Variable Name, Description, Placeholder, Default Value, Required (yes/no)
- **Use case**: Single-line text input (names, URLs, short queries)

### 2. Long Text
- **Parameters**: Input Label, Variable Name, Description, Placeholder, Default Value, Required (yes/no)
- **Use case**: Multi-line text input (paragraphs, detailed descriptions)

### 3. Checkbox
- **Parameters**: Input Label, Variable Name, Description, Default Value (checked/unchecked), Required (yes/no)
- **Use case**: Boolean toggle (yes/no, enable/disable)

### 4. Number
- **Parameters**: Input Label, Variable Name, Description, Placeholder, Default Value, Required (yes/no)
- **Use case**: Numeric input (quantities, prices, ratings)

### 5. File Upload
- **Parameters**: Input Label, Variable Name, Description, Required (yes/no)
- **Use case**: File attachments (documents, images, data files)

### 6. Audio Record
- **Parameters**: Input Label, Variable Name, Description, Required (yes/no)
- **Use case**: Voice recordings for transcription or analysis

### 7. Dropdown List
- **Parameters**: Input Label, Variable Name, Description, Options (list of choices), Default Value, Required (yes/no)
- **Use case**: Selection from predefined options

### 8. Time
- **Parameters**: Input Label, Variable Name, Description, Default Value, Required (yes/no)
- **Use case**: Time/date input for scheduling or time-based workflows

---

## Scheduled Time (Automation)

Cronjob component for automated flow execution at specified intervals.

| Parameter | Details |
|-----------|---------|
| **Timezone** | GMT -12 to GMT +12 |
| **Interval type** | Minute, Hours, Day, Week, Month |
| **Every** | Recurrence frequency (e.g., every 5 minutes, every 2 hours) |
| **On** | Day number (1-31) for monthly, or weekday name for weekly |
| **At** | Time in HH:mm format |
| **Starting date** | Start date in MM/DD/YYYY format |

Examples:
- Every 30 minutes starting from a specific date
- Every day at 09:00 GMT+7
- Every Monday at 08:00
- On the 1st of every month at 00:00

---

## Webhook (Automation)

Real-time data transmission between applications via HTTP endpoints.

| Parameter | Purpose |
|-----------|---------|
| **Webhook endpoint** | Two URLs provided: **Test URL** (for Draft/testing) and **Production URL** (for Published flows) |
| **API Key** | Selectable from workspace API Keys (created in Settings > API Keys) |
| **Body** | Data keys defined as **required** or **optional** fields |

How it works:
1. Configure the webhook trigger with body field definitions
2. Use the Test URL during development to send test payloads
3. After publishing, switch to the Production URL for live integrations
4. External systems send HTTP POST requests to the webhook URL with the defined body fields
5. The API Key must be included in requests for authentication

---

## Microsoft Outlook (Automation)

Triggers a flow based on Microsoft Outlook email events.

### 4 Trigger Event Types:
1. **New email received** -- Fires when any new email arrives in the inbox
2. **New attachment** -- Fires when an email with a new attachment is received
3. **New email matching search criteria** -- Fires when an email matches specified search filters
4. **New message in folder** -- Fires when a new email appears in a specific folder

### Setup:
- Connect your Microsoft Outlook account via the Account connection interface
- Select the desired trigger event type
- Configure event-specific parameters (search criteria, folder name, etc.)

---

## AI Chat & Agent Trigger

For AI Agent/Chatbot flows, the trigger accepts conversational input.

### Two Modes:
- **Simple mode** -- Basic configuration, select vector sources for knowledge base, configure AI engine
- **Advanced mode** -- Full trigger configuration with access to all component settings

### Attachment Toggle:
- Toggle attachments ON to allow users to upload files during chat
- Supported file types depend on the connected AI model capabilities

---

## Outputs

Outputs are the final nodes that display processed results to the user. Multiple output nodes can be used in a single flow.

---

### Text Output

Displays computed text results.

| Parameter | Description |
|-----------|-------------|
| **Title** | Label displayed above the output |
| **Value** | Content to display -- use `@` to reference other component outputs |
| **Markdown format** | Toggle ON to render output as formatted Markdown |

Features: Copy to clipboard, clear, download as file.

---

### Chart Output

Transforms data into visual charts.

| Parameter | Description |
|-----------|-------------|
| **Input** | Accepts JSON data from upstream components |
| **Chart types** | Bar, Line, Pie, Donut, Area, Column, Stacked, Grouped, Multi-line (auto-detected or specified via Convert JSON to Chart Data component) |

The JSON data structure determines the chart rendering. Use the "Convert JSON to Chart Data" built-in tool for precise chart type control.

---

### Video Output

Displays video content within the flow output.

| Parameter | Description |
|-----------|-------------|
| **Input** | Accepts `.mp4` video files from upstream components |
| **Source** | Typically from Video Generation components (BytePlus Seedance) |

Note: Video URLs from generation components expire in 24 hours.

---

### Audio Output

Plays back and provides download for audio content.

| Parameter | Description |
|-----------|-------------|
| **Input** | Audio data from Text-to-Speech components |
| **Features** | Playback controls, adjustable playback speed, download capability |
| **Formats** | MP3, OPUS, AAC, FLAC (depending on TTS component configuration) |

Sources: OpenAI TTS/TTS-HD, ElevenLabs Cloud, built-in Text-to-Speech AI Tool.

---

### Image Output

Displays generated or processed images.

| Parameter | Description |
|-----------|-------------|
| **Input** | Image data from Text-to-Image or image processing components |
| **Features** | Image display, download capability |
| **Sources** | DALL-E 3, BytePlus Seedream, Gemini Flash Image, built-in Image Generation AI Tool |
