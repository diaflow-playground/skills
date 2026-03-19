# Components Guide

## Component Categories

| Category | Examples | Description |
|----------|----------|-------------|
| **Triggers** | Apps input, Scheduled time, Webhook, Outlook, AI Chat | Entry points that initiate a flow |
| **Outputs** | Text, Chart, Video, Audio, Image | Display processed results to users |
| **Built-in Tools** | Branch, Merge, Split Data, Web Scraper, Loop, Delay, HTTP Request, SMTP, Filter, File Converter, QR Code Generator, Run Another Flow | Core utility components for flow logic and data processing |
| **Built-in Resources** | Diaflow Vision, Diaflow Vectors, Diaflow Drive, Diaflow Table, Diaflow Pages | Native Diaflow platform resources |
| **Private AI/LLM** | OpenAI, Anthropic, Llama (Meta), Google Gemini, BytePlus, Cohere, MistralAI | AI models hosted on Diaflow servers (data stays private) |
| **Public AI/LLM (BYOK)** | OpenAI Cloud, Perplexity Cloud, Deepseek Cloud, Anthropic Cloud, Google Gemini Cloud, Azure Cloud, AWS Bedrock Cloud, ElevenLabs Cloud, and more | Bring-your-own-key models using user-supplied API credentials |
| **Databases** | MySQL, Microsoft SQL, PostgreSQL, Snowflake | Direct database connections for query, add, and update operations |
| **Apps (Integrations)** | Gmail, Slack, Google Sheets, Salesforce, Telegram, Python, and 60+ more | Third-party app connections organized by category |
| **AI Tools** | Text Generation from Image, Audio Transcription, Image Generation, Entity Recognition, Text Summarization, Text-to-Speech, Data Classification | Built-in AI capabilities for common tasks |

## How Components Connect

- Data moves through flows via **component connections** (lines between nodes)
- Components only accept **compatible data types**
- During execution, components run **sequentially** following the connection path
- Flows can function as **API endpoints** when published

## Component Parameters and Configuration

- Most components include **configuration parameters** (e.g., model selection dropdowns, prompt fields, format options)
- Access additional options by selecting **"Show Advanced Configurations"**
- Advanced configs include: flow cache adjustment, answer precision calibration, temperature, max tokens, Top P, and more
- Some components support **caching** to avoid redundant processing

## Node ID Naming Patterns

Each component instance in a flow receives a unique node ID following these patterns:

| Component Type | Node ID Pattern | Examples |
|---------------|----------------|----------|
| Trigger | `trigger` (fixed) | `trigger` |
| Output | `output` (fixed) | `output` |
| OpenAI | `openai-{index}` | `openai-0`, `openai-1` |
| Branch | `branch-{index}` | `branch-0` |
| Python | `py-{index}` | `py-0` |
| JSON Formatter | `json-formatter-{index}` | `json-formatter-0` |
| PDF to Image | `pdf-img-{index}` | `pdf-img-0` |
| Database | `ddb-{index}` | `ddb-0` |
| Google Sheets | `google_sheets_p-{index}` | `google_sheets_p-0` |
| Sticky Notes | `stn-{index}` | `stn-0` |
| Other components | `{type}-{index}` | `web-scraper-0`, `smtp-0` |

The index increments for each additional instance of the same component type (starting from 0).

## Component Output Identifiers

Each component instance gets a **unique output identifier** used for referencing its data:
- `trigger.text` -- text input from the trigger
- `trigger.file` -- file input from the trigger
- `openai-0.output` -- output from the first OpenAI node
- `branch-0.output` -- output from the first Branch node
- `web-scraper-0.output` -- output from the first Web Scraper node

## Data Flow Referencing

To reference another component's output in any input field:
1. Type `@` in the input field
2. A dropdown appears listing all available component outputs
3. Select the desired output to create a dynamic reference

This enables chaining components together -- for example, passing the trigger's text input to an OpenAI prompt, then passing the OpenAI output to a Text Output node.
