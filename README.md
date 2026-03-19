# Diaflow Skill

A Claude Code plugin for building, deploying, and debugging [Diaflow](https://diaflow.io) workflows autonomously.

## What it does

This skill turns Claude Code into an autonomous Diaflow workflow architect. It handles the full lifecycle:

- **Create** workflows from natural language descriptions
- **Update** existing flows with new nodes, logic, or integrations
- **Validate** workflow JSON before deployment
- **Deploy** directly to Diaflow via API
- **Debug** flows with an autonomous test-and-fix loop

Supports all Diaflow flow types: AI Chatbots, Apps & Tools, Automations, and Scheduled tasks.

## Installation

```bash
claude plugin install <your-repo-url>
```

Or clone the repo and install locally:

```bash
git clone https://github.com/thuantan2060/diaflow-skill.git
claude plugin install ./diaflow-skill
```

## Setup

1. **Set your Diaflow token** — the skill will guide you through this on first use:
   - Mac/Linux: `bash skills/diaflow-maker/scripts/setup_token.sh`
   - Windows: `powershell -ExecutionPolicy Bypass -File skills/diaflow-maker/scripts/setup_token.ps1`

2. Start using it by telling Claude what you want to build:
   - "Create a chatbot that answers questions about my products"
   - "Build an automation that scrapes a website daily and emails a summary"
   - "Update my flow JlFO1d16b9 to add inventory tracking"
   - "Debug my chatbot AbCd1234"

## What's included

| Component | Description |
|-----------|-------------|
| `skills/diaflow-maker/SKILL.md` | Main skill definition with CREATE, UPDATE, and DEBUG workflows |
| `skills/diaflow-maker/references/` | Platform docs, API reference, node configs, OpenAPI spec |
| `skills/diaflow-maker/templates/` | Starter JSON templates (chatbot, form app, webhook, scheduled, pipeline) |
| `skills/diaflow-maker/scripts/` | Validation, fetch, debug, and token setup scripts |
| `skills/diaflow-maker/data/` | Component registry (node types, IDs, configs) |

## Requirements

- Python 3.8+ (for validation and debug scripts)
- A [Diaflow](https://diaflow.io) account with an active workspace
- `curl` (for API deployment)

## License

MIT
