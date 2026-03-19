# Diaflow Platform Overview

## What is Diaflow?

Diaflow is an autonomous AI agent platform that makes sophisticated workflow automation accessible to everyone, regardless of technical expertise. Unlike traditional automation tools with static triggers and rigid rules, Diaflow's autonomous AI agents understand context, make intelligent decisions, and handle complexity at scale.

Core offerings:
- **AI Chat** -- Interact with workflows, data, and agents in natural language
- **Flow Builder** -- Design and deploy automation workflows visually, no coding required
- **Productivity Suite** -- Complete toolkit (Tables, Drive, Vectors, Pages)
- **1,000+ Integrations** -- Connect to existing business apps

Backed by Insignia Ventures Partners and supported by AWS, Microsoft, Google, and NVIDIA. Over 10,000+ active users globally.

## Flow Types

| Type | Trigger Method | Description |
|------|---------------|-------------|
| **Automation** | Auto-triggered via webhooks, schedules, or emails | Workflows that run automatically in response to events |
| **Apps & Tools** | Manually triggered via forms/buttons | Interactive applications with user-facing input fields |
| **AI Agent/Chatbots** | AI-powered conversational interface | Smart workflows with chat-based interaction |

## Interface Types (API)

When working with flows programmatically, the following interface types are used:
- `form` -- Apps & Tools with form-based input
- `chat` -- AI Agent/Chatbot conversational interface
- `automation` -- Event-driven automated workflows
- `scheduled` -- Time-based automated workflows (cronjob)

## Terminology Glossary

| Term | Definition |
|------|-----------|
| **API** | A set of rules and protocols for software communication |
| **API Key** | Unique code for authenticating API access |
| **Branch** | Algorithmic component dividing output into separate conditional paths |
| **Component** | An element performing a specific function in a flow |
| **Config** | Settings area for flow parameters |
| **Drive** | Centralized file storage system accessible by any flow in the workspace |
| **Flow** | Collection of interconnected components forming a workflow |
| **GenAI** | Generative AI systems that create original content (text, images, etc.) |
| **Input** | Data provided for processing |
| **Integrations** | Connecting different software systems via stored third-party API credentials |
| **LLM** | Large Language Models for understanding and generating human language |
| **Model** | Machine learning system for generating content |
| **Node** | Fundamental unit in a flow (synonymous with component instance) |
| **Output** | Result produced after processing |
| **Preview** | View content before finalizing |
| **SMTP** | Simple Mail Transfer Protocol for automated email delivery |
| **Spreadsheet** | Software for tabular data management |
| **Tables** | Structured data storage with rows and columns (a Diaflow productivity tool) |
| **Templates** | Pre-designed flow formats available in the Community marketplace |
| **Trigger** | Event or input that initiates a flow |
| **Vectors** | Numerical data representations stored for semantic search (vector database) |
| **Web scraper** | Tool for extracting data from website URLs |
| **Workspace** | Virtual environment for organizing projects, flows, and team resources |

## Credit System

Credits measure the resources consumed when running flows. They reset monthly and additional credits can be purchased.

| Unit Type | Applies To | Formula |
|-----------|-----------|---------|
| **Token** | AI/LLM text nodes | (Input credits x Input tokens) + (Output credits x Output tokens) |
| **Character** | AI/LLM text nodes | Output Credits x Number of characters |
| **Image** | Image generation nodes | Output Credits x Number of images |
| **Second** | Time-based AI nodes (TTS, STT) | Output Credits x Duration (seconds) |
| **Request** | App category nodes | Output credit per run |

Nodes that do not consume credits are indicated as free in the Component List popup.

## How a Flow Works

A flow represents a structured process with three phases:

1. **Trigger (Input Stage)** -- Accepts various media types: audio, text, images, video, files
2. **Components (Processing Stage)** -- One or more elements that transform input data and produce results
3. **Output (Result Stage)** -- Displays the processed results (text, charts, images, audio, video)

## How a Component Works

Components execute specific tasks within a flow by:
- Accepting inputs (from the trigger or from other components)
- Generating outputs (referenced by downstream components)
- Providing advanced configuration options (flow cache, answer precision, model selection, etc.)

Data moves between components via connections. Components only accept compatible data types. Type `@` in any input field to reference outputs from other components.

## Getting Started

1. Click "New" and choose a flow type (Automation, Apps & Tools, AI Agent/Chatbots)
2. Configure the Trigger node with input fields
3. Add processing components (AI models, tools, integrations)
4. Configure the Output node to display results
5. Click "Execute" to test, then "Publish" to deploy

Alternatively, browse the Community for pre-built templates and clone them to your workspace.
