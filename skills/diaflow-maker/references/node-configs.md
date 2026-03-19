# Node Configuration Reference

Per-node-type documentation of the `data` field structure for Diaflow workflow JSON.
Use this reference when generating `FlowNode.data` objects.

---

## trigger

- **ID**: `trigger` (fixed)
- **Type**: `trigger`

### App Flow

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| inputs | array | yes | Array of input field objects |

Each input object:
```json
{
  "type": "short-text"|"long-text"|"checkbox"|"number"|"file-upload"|"audio"|"dropdown"|"time",
  "label": "string",
  "variableName": "string",
  "required": true|false,
  "placeholder": "string",
  "defaultValue": "string",
  "description": "string"
}
```

### Automation - Scheduled

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| triggerType | string | yes | `"scheduled"` |
| cronjob | object | yes | Schedule configuration |

Cronjob object:
```json
{
  "timezone": "string",
  "intervalType": "string",
  "every": "number",
  "on": "string",
  "at": "string",
  "starting": "string"
}
```

### Automation - Webhook

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| triggerType | string | yes | `"webhook"` |
| webhook | object | yes | Webhook configuration |

Webhook object:
```json
{
  "endpoint": "string",
  "apiKey": "string",
  "body": [{ "key": "string", "required": true|false }]
}
```

### Chat Flow

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| triggerType | string | yes | `"chat"` |
| attachments | boolean | no | Enable file attachments |

**Connections**: No inputs. Outputs connect to any node.

---

## openai

- **ID pattern**: `openai-{n}` (e.g., `openai-0`, `openai-1`)
- **Type**: `openai`

### Text Generation (GPT)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| model | string | yes | - | `"gpt-5"`, `"gpt-5-mini"`, `"gpt-4o"`, `"gpt-4.1"`, etc. |
| prompt | string | yes | - | Prompt text, supports `{{nodeId.output}}` references |
| systemMessage | string | no | - | System instruction |
| temperature | number | no | varies | 0-1 |
| maxTokens | integer | no | - | 0-3097 |
| topP | number | no | - | 0-1 |
| presencePenalty | number | no | - | -2 to 2 |
| frequencyPenalty | number | no | - | -2 to 2 |
| memory | boolean | no | false | Enable conversation memory |
| windowSize | integer | no | - | 0-5 memory window |
| caching | boolean | no | false | Enable response caching |
| cachingTime | integer | no | - | Cache TTL |
| connection | string | no | `"diaflow"` | `"diaflow"` or credential ID |

Minimal example:
```json
{
  "model": "gpt-4o",
  "prompt": "Summarize: {{trigger.output}}"
}
```

### Image Generation (DALL-E)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| model | string | yes | `"dall-e-3"` |
| prompt | string | yes | Image description |
| quantity | integer | no | Number of images |
| size | string | no | Image dimensions |

### Text-to-Speech (TTS)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| model | string | yes | `"tts"` or `"tts-hd"` |
| voice | string | yes | Voice selection |
| input | string | yes | Text to speak |
| responseFormat | string | no | `"mp3"`, `"opus"`, `"aac"`, `"flac"` |
| speed | number | no | Speech speed |

### Speech-to-Text (Whisper)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| model | string | yes | `"whisper-1"` |
| endpoint | string | yes | `"transcriptions"` or `"translations"` |
| language | string | no | Source language |

**Connections**: Accepts text/image/audio input. Outputs text/image/audio.

---

## anthropic

- **ID pattern**: `an-{n}`
- **Type**: `anthropic`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| model | string | yes | `"claude-4.5-sonet"`, `"claude-4.5-opus"`, `"claude-4.5-haiku"` |
| prompt | string | yes | Supports `{{nodeId.output}}` references |
| temperature | number | no | 0-1 |
| maxTokens | integer | no | Max output tokens |
| topP | number | no | 0-1 |
| caching | boolean | no | Enable caching |
| memory | boolean | no | Enable memory |
| imageSource | string | no | Image input reference |

Minimal example:
```json
{
  "model": "claude-4.5-sonet",
  "prompt": "Analyze: {{trigger.output}}"
}
```

**Connections**: Accepts text input. Outputs text.

---

## llama

- **ID pattern**: `an-{n}`
- **Type**: `llama`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| model | string | yes | Llama 3 8B through Llama 4 Maverick 17B variants |
| prompt | string | yes | Supports `{{nodeId.output}}` references |
| caching | boolean | no | Enable caching |
| imageSource | string | no | Image input reference |

Minimal example:
```json
{
  "model": "llama-3-8b",
  "prompt": "{{trigger.output}}"
}
```

**Connections**: Accepts text input. Outputs text.

---

## gemini

- **ID pattern**: `gg-{n}`
- **Type**: `google-gemini`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| model | string | yes | - | `"gemini-2.5-pro"`, `"gemini-2.5-flash"`, `"gemini-2.0-flash"`, `"gemini-2.0-flash-lite"` |
| prompt | string | yes | - | Supports `{{nodeId.output}}` references |
| temperature | number | no | - | 0-1 |
| maxTokens | integer | no | - | Max output tokens |
| topP | number | no | - | 0-1 |
| caching | boolean | no | false | Enable caching |
| memory | boolean | no | false | Enable memory |
| windowSize | integer | no | - | 0-1000 memory window |

Minimal example:
```json
{
  "model": "gemini-2.5-flash",
  "prompt": "{{trigger.output}}"
}
```

**Connections**: Accepts text input. Outputs text.

---

## byteplus

- **ID pattern**: `byteplus-{n}`
- **Type**: `byteplus`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| model | string | yes | `"deepseek-v3.2"`, `"seed-1.6"`, `"seedream-4.5"`, `"seedance-1.0-pro"`, `"seedance-1.5-pro"` |
| prompt | string | yes | Supports `{{nodeId.output}}` references |
| imageSource | string | no | Image input reference |
| resolution | string | no | Output resolution |
| aspectRatio | string | no | Aspect ratio |
| duration | string | no | `"5s"` or `"12s"` (video) |
| numImages | integer | no | 1-4 |
| audio | string | no | Audio config |
| enhancement | string | no | Enhancement config |
| compression | string | no | Compression config |

**Connections**: Accepts text/image input. Outputs text/image/video.

---

## cohere

- **ID pattern**: `an-{n}`
- **Type**: `cohere`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| model | string | yes | `"command-r+"`, `"command-r"` |
| prompt | string | yes | Supports `{{nodeId.output}}` references |
| caching | boolean | no | Enable caching |
| imageSource | string | no | Image input reference |

**Connections**: Accepts text input. Outputs text.

---

## mistral

- **ID pattern**: `an-{n}`
- **Type**: `mistral`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| model | string | yes | `"mistral-7b"`, `"mixtral-8x7b"`, `"mistral-small"`, `"mistral-large"`, `"pixtral-large"` |
| prompt | string | yes | Supports `{{nodeId.output}}` references |
| caching | boolean | no | Enable caching |
| imageSource | string | no | Image input reference |

**Connections**: Accepts text input. Outputs text.

---

## branch

- **ID pattern**: `branch-{n}`
- **Type**: `branch`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| conditions | array | yes | Array of condition objects |

Each condition:
```json
{
  "field": "{{nodeId.output}}",
  "operator": "contains",
  "value": "string"
}
```

**Operators**: `contains`, `does-not-contain`, `matches`, `does-not-match`, `starts-with`, `ends-with`, `file-format`, `number-equals`, `number-greater`, `number-less`, `date-equal`, `date-after`, `date-before`, `is-true`, `is-false`, `exists`, `does-not-exist`, `is-null`, `is-not-null`

Creates `path-{n}` sub-nodes for each branch. Each path connects to downstream nodes independently.

**Connections**: Accepts any input. Outputs multiple paths.

---

## json-formatter

- **ID pattern**: `json-formatter-{n}`
- **Type**: `json-formatter`

Merges data from multiple sources into unified JSON format.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| inputs | array | yes | Array of input references (e.g., `["{{openai-0.output}}", "{{an-0.output}}"]`) |

**Connections**: Accepts multiple inputs from any node. Outputs unified JSON.

**Example data:**
```json
{
  "inputs": [
    "{{openai-0.output}}",
    "{{scraper-0.output}}"
  ]
}
```

---

## stn (Split Data / JSON Formatter)

- **ID pattern**: `stn-{n}`
- **Type**: `stn`

Formats output data into well-structured JSON.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| input | string | yes | Reference to input data (e.g., `"{{openai-0.output}}"`) |

**Connections**: Accepts JSON input. Outputs formatted JSON.

---

## filter

- **ID pattern**: `filter-{n}`
- **Type**: `filter`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| conditions | array | yes | Same condition format and operators as branch |
| logic | string | yes | `"AND"` or `"OR"` group logic |

Binary gate: flow passes or halts. No branching.

**Connections**: Accepts any input. Outputs pass or halt.

---

## output

- **ID**: `output` (fixed)
- **Type**: `output`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| outputs | array | yes | Array of output display objects |

Each output object:
```json
{
  "type": "text"|"chart"|"video"|"audio"|"image",
  "title": "string",
  "value": "{{nodeId.output}}"
}
```

**Connections**: Accepts any input. Terminal node (no outputs).

---

## loop

- **ID pattern**: `loop-{n}`
- **Type**: `loop`

### Loop Over Items

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| input | string | yes | - | JSON string (array to iterate) |
| batchSize | integer | no | 1 | Items per batch |
| onError | string | no | `"skip"` | `"skip"` or `"stop"` |

### Loop Output

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| dataToStore | string | yes | Variable name from each iteration |

Maximum 100 runs per session.

**Connections**: Accepts JSON/array input. Outputs aggregated array.

---

## http-request

- **ID pattern**: `http-request-{n}`
- **Type**: `http-request`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| method | string | yes | - | `"GET"`, `"POST"`, `"PUT"`, `"PATCH"`, `"DELETE"` |
| url | string | yes | - | Target URL |
| headers | array | no | - | `[{key, value}]` |
| parameters | array | no | - | `[{key, value}]` query params |
| payload | array | no | - | `[{key, value}]` body fields |
| failureStrategy | string | no | `"stop"` | `"stop"`, `"skip"`, `"retry"` |
| maxRetry | integer | no | - | 1-3 (when strategy is retry) |
| retryDelay | integer | no | - | 1-5 seconds |

**Connections**: No required input. Outputs text/JSON.

---

## smtp

- **ID pattern**: `smtp-{n}`
- **Type**: `smtp`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| credentials | string | yes | SMTP credential ID |
| to | string | yes | Recipient email |
| object | string | yes | Email subject |
| message | string | yes | Email body |
| cc | string | no | CC recipients |
| attachments | string | no | File attachments |

**Connections**: Accepts text input. No output.

---

## web-scraper

- **ID pattern**: `scraper-{n}`
- **Type**: `scraper`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| url | string | yes | - | URL to scrape |
| outputFormat | string | no | `"html"` | `"html"`, `"markdown"`, `"plaintext"` |
| caching | boolean | no | false | Enable caching |
| cachingTime | integer | no | - | Cache TTL |

**Connections**: No required input. Outputs text/HTML.

---

## dtt (Document to Text)

- **ID pattern**: `dtt-{n}`
- **Type**: `dtt`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| data | string | yes | Document file reference |
| caching | boolean | no | Enable caching |
| cachingTime | integer | no | Cache TTL |

**Connections**: Accepts file input. Outputs text.

---

## tbl-analyzer (Spreadsheet Analyzer)

- **ID pattern**: `tbl-analyzer-{n}`
- **Type**: `tbl-analyzer`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| data | string | yes | Spreadsheet/CSV file reference |
| action | string | yes | `"query"` |
| sqlGenerateMethod | string | yes | `"ai"` or `"manual"` |
| input | string | yes | Query or SQL statement |
| caching | boolean | no | Enable caching |

**Connections**: Accepts file input. Outputs text/data.

---

## spreadsheet-creator

- **ID pattern**: `spreadsheet-creator-{n}`
- **Type**: `spreadsheet-creator`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| inputData | string | yes | @ reference to JSON data |
| format | string | yes | `"csv"`, `"xlsx"`, `"xls"` |

**Connections**: Accepts JSON input. Outputs file.

---

## json-chart

- **ID pattern**: `json-chart-{n}`
- **Type**: `json-chart`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| input | string | yes | JSON data reference |
| chartType | string | yes | One of 13 chart types |
| caching | boolean | no | Enable caching |

**Connections**: Accepts JSON input. Outputs chart.

---

## pdf-img (PDF to Image)

- **ID pattern**: `pdf-img-{n}`
- **Type**: `pdf-img`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| input | string | yes | PDF file reference |
| pagesPerImage | integer | yes | Pages per image (min 2) |
| caching | boolean | no | Enable caching |

**Connections**: Accepts file input. Outputs image.

---

## date-time

- **ID pattern**: `date-time-{n}`
- **Type**: `date-time`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| retrievalData | object | yes | Day/date/time selection flags |
| dayFormat | string | no | Day format string |
| dateFormat | string | no | Date format string |
| timeFormat | string | no | Time format string |
| timezone | string | no | Timezone identifier |

**Connections**: No input required. Outputs text.

---

## weather

- **ID pattern**: `weather-{n}`
- **Type**: `weather`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | string | yes | `"current"`, `"forecast"`, `"history"` |
| inputMethod | string | yes | Location input method |
| value | string | yes | Location value |
| day | integer | no | Forecast days (1-14) |
| startDate | string | no | History start date |
| endDate | string | no | History end date |

**Connections**: No input required. Outputs text.

---

## geo (GEO Location)

- **ID pattern**: `geo-{n}`
- **Type**: `geo`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| method | string | yes | `"auto"` or `"manual"` |
| dataToRetrieve | string | yes | `"lat-long"` or `"city"` |
| value | string | no | Manual location value |

**Connections**: No input required. Outputs text.

---

## delay

- **ID pattern**: `delay-{n}`
- **Type**: `delay`

### Option A: Delay For

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| delayType | string | yes | `"for"` |
| unit | string | yes | `"seconds"`, `"minutes"`, `"hours"` |
| duration | number | yes | Duration value |

### Option B: Delay Until

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| delayType | string | yes | `"until"` |
| dateTime | string | yes | ISO datetime string |

**Connections**: No required input. No output (passes through).

---

## file-converter

- **ID pattern**: `file-converter-{n}`
- **Type**: `file-converter`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| originalFile | string | yes | Source file reference |
| originalFormat | string | yes | Source format |
| targetFormat | string | yes | Target format |

**Connections**: Accepts file input. Outputs file.

---

## file-creator

- **ID pattern**: `file-creator-{n}`
- **Type**: `file-creator`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| fileType | string | yes | Output file type |
| fileName | string | yes | Output file name |
| content | string | yes | File content |

**Connections**: Accepts text input. Outputs file.

---

## qr-code

- **ID pattern**: `qr-code-{n}`
- **Type**: `qr-code`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| inputUrl | string | yes | - | URL to encode |
| size | integer | no | - | QR code size |
| bgColor | string | no | - | Background color |
| fgColor | string | no | - | Foreground color |
| format | string | no | - | Output format |
| outputType | string | no | - | Output type |

**Connections**: Accepts text input. Outputs image.

---

## run-flow

- **ID pattern**: `run-flow-{n}`
- **Type**: `run-flow`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| flowId | string | yes | Target flow ID to execute |
| fieldInput | object | no | Input fields for the sub-flow |
| onError | string | no | Error handling strategy |

Only works with App-type flows. Executes synchronously.

**Connections**: Accepts any input. Outputs sub-flow result.

---

## image-gen

- **ID pattern**: `image-gen-{n}`
- **Type**: `image-gen`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| model | string | yes | Generation model (Gemini/BytePlus) |
| prompt | string | yes | Image description |
| imageSource | string | no | Reference image |
| aspectRatio | string | no | Output aspect ratio |
| numImages | integer | no | Number of images |

**Connections**: Accepts text input. Outputs image.

---

## video-gen

- **ID pattern**: `video-gen-{n}`
- **Type**: `video-gen`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| model | string | yes | Video model (BytePlus Seedance) |
| prompt | string | yes | Video description |
| imageSource | string | no | Reference image |
| resolution | string | no | Output resolution |
| aspectRatio | string | no | Aspect ratio |
| duration | string | no | `"5s"` or `"12s"` |
| audio | string | no | Audio config |
| enhancement | string | no | Enhancement config |
| compression | string | no | Compression config |

**Connections**: Accepts text input. Outputs video.

---

## diaflow-vision

- **ID pattern**: `diaflow-vision-{n}`
- **Type**: `diaflow-vision`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| prompt | string | yes | Analysis prompt |
| imageSource | string | yes | Image reference |
| maxToken | integer | no | Max output tokens |
| caching | boolean | no | Enable caching |

**Connections**: Accepts image input. Outputs text.

---

## vec (Diaflow Vectors)

- **ID pattern**: `vec-{n}`
- **Type**: `vec`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| action | string | yes | `"search"` or `"add"` |
| input | string | yes | Search query or data to add |
| destination | string | no | Target vector store |
| selectData | string | no | Data selection filter |

**Connections**: Accepts text/file input. Outputs text/data.

---

## drive (Diaflow Drive)

- **ID pattern**: `drive-{n}`
- **Type**: `drive`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| action | string | yes | `"save"`, `"get-url"`, `"file-metadata"`, `"folder-metadata"` |
| folder | string | no | Target folder |
| fileData | string | no | File data reference |
| from | string | no | Source reference |
| selectFile | string | no | File selection |

**Connections**: Accepts file input. Outputs file/text.

---

## ddb (Diaflow Table)

- **ID pattern**: `ddb-{n}`
- **Type**: `ddb`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| action | string | yes | `"query"`, `"add"`, `"update"` |
| table | string | yes | Target table name |
| sqlGenerateMethod | string | no | `"ai"` or `"manual"` |
| input | string | no | Query or data |
| caching | boolean | no | Enable caching |

**Connections**: Accepts text input. Outputs text/data.

---

## diaflow-page

- **ID pattern**: `diaflow-page-{n}`
- **Type**: `diaflow-page`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| action | string | yes | `"add-existing"`, `"add-new"`, `"retrieve"` |
| page | string | no | Page reference (for existing) |
| title | string | no | Page title (for new) |
| content | string | no | Page content |

**Connections**: Accepts text input. Outputs text.

---

## py (Python Code)

- **ID pattern**: `py-{n}`
- **Type**: `py`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| code | string | yes | Python code to execute |
| packages | array | no | Additional pip packages |

**Connections**: Accepts any input. Outputs any.

---

## google_sheets_p

- **ID pattern**: `google_sheets_p-{n}`
- **Type**: `google_sheets_p`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| credentials | string | yes | Google credential ID |
| spreadsheetId | string | yes | Spreadsheet ID |
| sheetName | string | yes | Sheet tab name |
| action | string | yes | Operation type |

**Connections**: Accepts data input. Outputs data.

---

## mysql / postgresql / mssql / snowflake

- **ID pattern**: `{type}-{n}` (e.g., `mysql-0`)
- **Type**: `mysql`, `postgresql`, `mssql`, `snowflake`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| resource | string | yes | Database credential/connection ID |
| table | string | yes | Target table |
| action | string | yes | Operation type |
| sqlGenerateMethod | string | yes | `"ai"` or `"manual"` |
| input | string | no | Query or data |
| codeEditor | string | no | Manual SQL code |

**Connections**: Accepts text input. Outputs data.
